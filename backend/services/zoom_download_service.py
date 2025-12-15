"""
Zoom Download Service

This service handles downloading chat messages from Zoom API
and integrates with the existing Flask application architecture.
"""

import os
import json
import time
from typing import List, Dict, Optional, Callable
from datetime import datetime, timedelta
import logging
from dotenv import load_dotenv

from backend.utils.config import Config
from backend.core.interfaces import IZoomDownloadService
from backend.services.zoom_api_client import ZoomAPIClient

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class ZoomDownloadService(IZoomDownloadService):
    """Service for downloading Zoom chat messages"""
    
    def __init__(self):
        try:
            self.api_client = ZoomAPIClient()
            logger.info("ZoomDownloadService initialized")
        except ValueError as e:
            logger.error(f"Failed to initialize ZoomDownloadService: {e}")
            raise
        except Exception as e:
            # Don't fail initialization if OAuth fails - we'll check later
            logger.warning(f"ZoomDownloadService initialized but OAuth may fail: {e}")
            self.api_client = None
    
    def download_chat_messages(self, start_date: str, end_date: str,
                               progress_callback: Optional[Callable] = None,
                               max_duration_minutes: int = 30) -> None:
        """
        Download chat messages for a date range
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            progress_callback: Optional callback(current, total, downloaded, failed)
            max_duration_minutes: Maximum duration for download in minutes
        """
        if not self.api_client:
            # Try to initialize if not already done
            try:
                self.api_client = ZoomAPIClient()
            except Exception as e:
                raise ValueError(f"Zoom API client not available: {e}. Please check your Zoom credentials.")
        
        try:
            logger.info(f"Starting Zoom chat download: {start_date} to {end_date}")
            
            # Validate date format
            try:
                datetime.strptime(start_date, '%Y-%m-%d')
                datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError as e:
                raise ValueError(f"Invalid date format. Use YYYY-MM-DD format: {e}")
            
            # Generate output filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"zoom_chats_{timestamp}.jsonl"
            
            start_time = datetime.now()
            end_time = start_time + timedelta(minutes=max_duration_minutes)
            
            # Get all chat sessions
            logger.info("Fetching chat sessions...")
            if progress_callback:
                # Update phase to fetching_sessions
                progress_callback(0, 0, 0, 0, phase='fetching_sessions')
            
            sessions = self.api_client.get_all_chat_sessions(start_date, end_date)
            
            if not sessions:
                logger.warning("No chat sessions found in date range")
                if progress_callback:
                    progress_callback(0, 0, 0, 0, phase='completed')
                return
            
            total_sessions = len(sessions)
            logger.info(f"Found {total_sessions} chat sessions")
            
            # Initialize progress tracking
            downloaded_count = 0
            failed_count = 0
            total_messages = 0
            
            if progress_callback:
                progress_callback(0, total_sessions, 0, 0, phase='downloading_messages')
            
            # Download messages for each session
            try:
                with open(output_file, 'w', encoding='utf-8') as outfile:
                    for i, session in enumerate(sessions, 1):
                        # Check time limit
                        if datetime.now() >= end_time:
                            logger.info(f"Time limit reached ({max_duration_minutes} minutes). Stopping download.")
                            break
                        
                        session_id = session.get('session_id') or session.get('id')
                        if not session_id:
                            logger.warning(f"Session missing ID: {session}")
                            failed_count += 1
                            continue
                        
                        try:
                            logger.info(f"Processing session {i}/{total_sessions}: {session_id}")
                            
                            # Update progress with current session info
                            if progress_callback:
                                progress_callback(i, total_sessions, downloaded_count, failed_count, 
                                                current_session_id=session_id, phase='downloading_messages')
                            
                            # Get all messages for this session
                            messages = self.api_client.get_all_chat_messages(
                                session_id, start_date, end_date
                            )
                            
                            message_count = len(messages)
                            total_messages += message_count
                            
                            # Create data structure
                            session_data = {
                                'session_id': session_id,
                                'session_info': session,
                                'messages': messages,
                                'message_count': message_count,
                                '_metadata': {
                                    'downloaded_at': datetime.now().isoformat(),
                                    'date_range': {
                                        'start_date': start_date,
                                        'end_date': end_date
                                    },
                                    'session_number': i
                                }
                            }
                            
                            # Write to JSONL file
                            outfile.write(json.dumps(session_data) + '\n')
                            downloaded_count += 1
                            
                            # Update progress with message counts
                            if progress_callback:
                                progress_callback(i, total_sessions, downloaded_count, failed_count,
                                                current_session_id=session_id,
                                                messages_in_session=message_count,
                                                total_messages=total_messages,
                                                phase='downloading_messages')
                            
                            # Small delay to avoid rate limiting
                            time.sleep(0.2)
                            
                        except Exception as session_error:
                            logger.error(f"Error processing session {session_id}: {session_error}")
                            failed_count += 1
                            if progress_callback:
                                progress_callback(i, total_sessions, downloaded_count, failed_count,
                                                current_session_id=session_id,
                                                total_messages=total_messages,
                                                phase='downloading_messages')
                            continue
                
                elapsed_time = datetime.now() - start_time
                logger.info(f"Download completed!")
                logger.info(f"Time elapsed: {elapsed_time}")
                logger.info(f"Successfully downloaded: {downloaded_count} sessions")
                logger.info(f"Failed: {failed_count} sessions")
                logger.info(f"Total messages downloaded: {total_messages}")
                logger.info(f"Output saved to: {output_file}")
                
                # Update progress to uploading phase
                if progress_callback:
                    progress_callback(downloaded_count, total_sessions, downloaded_count, failed_count,
                                    total_messages=total_messages, phase='uploading_s3')
                
                # Upload to S3 if configured
                if Config.STORAGE_TYPE == 's3' and Config.S3_BUCKET_NAME:
                    try:
                        logger.info("Uploading to S3...")
                        self._upload_to_s3(output_file)
                        logger.info("S3 upload completed")
                    except Exception as s3_error:
                        logger.error(f"Failed to upload to S3: {s3_error}")
                
                # Mark as completed
                if progress_callback:
                    progress_callback(downloaded_count, total_sessions, downloaded_count, failed_count,
                                    total_messages=total_messages, phase='completed')
                
            except Exception as file_error:
                logger.error(f"Error writing to output file {output_file}: {file_error}")
                raise
                
        except Exception as e:
            logger.error(f"Error in download_chat_messages: {e}")
            import traceback
            logger.error(traceback.format_exc())
            raise
    
    def _upload_to_s3(self, local_file: str):
        """Upload downloaded file to S3"""
        try:
            # Generate S3 key with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            s3_key = f"zoom-chats/{timestamp}_{os.path.basename(local_file)}"
            
            logger.info(f"Uploading {local_file} to S3: s3://{Config.S3_BUCKET_NAME}/{s3_key}")
            
            # Use boto3 to upload the file
            import boto3
            s3_client = boto3.client('s3', region_name=Config.S3_REGION)
            
            with open(local_file, 'rb') as f:
                s3_client.put_object(
                    Bucket=Config.S3_BUCKET_NAME,
                    Key=s3_key,
                    Body=f,
                    ContentType='application/json'
                )
            
            logger.info(f"Successfully uploaded to S3: {s3_key}")
                
        except Exception as e:
            logger.error(f"Error uploading to S3: {e}")
            raise
    
    def get_download_statistics(self) -> Dict:
        """Get download statistics"""
        stats = {
            'total_downloaded': 0,
            'total_size_mb': 0,
            'files': []
        }
        
        try:
            for file in os.listdir('.'):
                if file.startswith('zoom_chats') and file.endswith('.jsonl'):
                    file_size = os.path.getsize(file)
                    file_mtime = datetime.fromtimestamp(os.path.getmtime(file))
                    
                    # Count sessions in file
                    session_count = 0
                    try:
                        with open(file, 'r', encoding='utf-8') as f:
                            for line in f:
                                if line.strip():
                                    session_count += 1
                    except Exception:
                        pass
                    
                    stats['files'].append({
                        'filename': file,
                        'size_mb': round(file_size / (1024 * 1024), 2),
                        'session_count': session_count,
                        'created_at': file_mtime.isoformat()
                    })
                    
                    stats['total_downloaded'] += session_count
                    stats['total_size_mb'] += file_size / (1024 * 1024)
            
            stats['total_size_mb'] = round(stats['total_size_mb'], 2)
            
        except Exception as e:
            logger.error(f"Error getting download statistics: {e}")
        
        return stats

