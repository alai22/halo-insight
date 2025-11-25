"""
Zoom Download Management API Routes

This module provides API endpoints for managing Zoom chat downloads
through the web interface.
"""

import os
import json
import threading
import time
import traceback
from datetime import datetime
from flask import Blueprint, request, jsonify
from typing import Dict, Optional
import logging
from dotenv import load_dotenv

from backend.services.zoom_download_service import ZoomDownloadService
from backend.utils.config import Config
from backend.utils.email_service import EmailService

# Load environment variables from .env file
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Create blueprint
zoom_bp = Blueprint('zoom', __name__, url_prefix='/api/zoom')

# Global download state
download_state = {
    'is_running': False,
    'current_session': 0,
    'total_sessions': 0,
    'downloaded_count': 0,
    'failed_count': 0,
    'start_time': None,
    'end_time': None,
    'error': None,
    'progress_percentage': 0
}

# Global download service instance
download_service: Optional[ZoomDownloadService] = None
download_thread: Optional[threading.Thread] = None


@zoom_bp.route('/download/status', methods=['GET'])
def get_download_status():
    """Get current download status"""
    try:
        # Calculate progress percentage
        if download_state['total_sessions'] > 0:
            download_state['progress_percentage'] = (download_state['current_session'] / download_state['total_sessions']) * 100
        
        # Calculate elapsed time
        elapsed_time = None
        if download_state['start_time']:
            elapsed_time = (datetime.now() - download_state['start_time']).total_seconds()
        
        return jsonify({
            'status': 'success',
            'data': {
                'is_running': download_state['is_running'],
                'current_session': download_state['current_session'],
                'total_sessions': download_state['total_sessions'],
                'downloaded_count': download_state['downloaded_count'],
                'failed_count': download_state['failed_count'],
                'progress_percentage': round(download_state['progress_percentage'], 2),
                'start_time': download_state['start_time'].isoformat() if download_state['start_time'] else None,
                'elapsed_time': elapsed_time,
                'error': download_state['error']
            }
        })
    except Exception as e:
        logger.error(f"Error getting download status: {e}\n{traceback.format_exc()}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@zoom_bp.route('/download/start', methods=['POST'])
def start_download():
    """Start a new download"""
    global download_service, download_thread, download_state
    
    try:
        # Check if download is already running
        if download_state['is_running']:
            logger.warning("Attempted to start download while one is already running")
            return jsonify({'status': 'error', 'message': 'Download is already running'}), 400
        
        # Get request data
        data = request.get_json() or {}
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        max_duration_minutes = data.get('max_duration_minutes', 30)
        
        logger.info(f"Starting Zoom download request: start_date={start_date}, end_date={end_date}, "
                   f"max_duration={max_duration_minutes}")
        
        # Validate date parameters
        if not start_date or not end_date:
            return jsonify({'status': 'error', 'message': 'start_date and end_date are required'}), 400
        
        if not isinstance(start_date, str) or not isinstance(end_date, str):
            return jsonify({'status': 'error', 'message': 'Dates must be strings in YYYY-MM-DD format'}), 400
        
        # Validate date range
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
            if start_date_obj > end_date_obj:
                return jsonify({'status': 'error', 'message': 'Start date must be before end date'}), 400
        except ValueError:
            return jsonify({'status': 'error', 'message': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        # Initialize download service
        try:
            download_service = ZoomDownloadService()
            logger.debug("Zoom download service initialized")
        except Exception as e:
            error_msg = f"Failed to initialize download service: {str(e)}"
            logger.error(f"{error_msg}\n{traceback.format_exc()}")
            return jsonify({'status': 'error', 'message': error_msg}), 500
        
        # Reset download state
        download_state.update({
            'is_running': True,
            'current_session': 0,
            'total_sessions': 0,
            'downloaded_count': 0,
            'failed_count': 0,
            'start_time': datetime.now(),
            'end_time': None,
            'error': None,
            'progress_percentage': 0
        })
        
        # Start download in background thread
        download_thread = threading.Thread(
            target=_run_download,
            args=(start_date, end_date, max_duration_minutes),
            daemon=True,
            name="ZoomDownloadThread"
        )
        download_thread.start()
        
        logger.info(f"Zoom download thread started: {start_date} to {end_date}")
        
        return jsonify({
            'status': 'success',
            'message': f'Download started for {start_date} to {end_date}',
            'data': {
                'start_date': start_date,
                'end_date': end_date,
                'max_duration_minutes': max_duration_minutes
            }
        })
        
    except Exception as e:
        error_msg = f"Error starting download: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        download_state['error'] = error_msg
        download_state['is_running'] = False
        return jsonify({'status': 'error', 'message': error_msg}), 500


@zoom_bp.route('/download/stop', methods=['POST'])
def stop_download():
    """Stop the current download"""
    global download_state
    
    try:
        if not download_state['is_running']:
            return jsonify({'status': 'error', 'message': 'No download is currently running'}), 400
        
        # Stop the download
        download_state['is_running'] = False
        download_state['end_time'] = datetime.now()
        
        logger.info("Zoom download stopped by user")
        
        return jsonify({
            'status': 'success',
            'message': 'Download stopped successfully'
        })
        
    except Exception as e:
        logger.error(f"Error stopping download: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@zoom_bp.route('/download/stats', methods=['GET'])
def get_download_stats():
    """Get overall download statistics"""
    try:
        if not download_service:
            download_service = ZoomDownloadService()
        
        stats = download_service.get_download_statistics()
        
        return jsonify({
            'status': 'success',
            'data': stats
        })
        
    except Exception as e:
        logger.error(f"Error getting download stats: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@zoom_bp.route('/download/history', methods=['GET'])
def get_download_history():
    """Get download file history"""
    try:
        if not download_service:
            download_service = ZoomDownloadService()
        
        stats = download_service.get_download_statistics()
        
        return jsonify({
            'status': 'success',
            'data': {
                'files': stats.get('files', []),
                'total_files': len(stats.get('files', [])),
                'total_sessions': stats.get('total_downloaded', 0),
                'total_size_mb': stats.get('total_size_mb', 0)
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting download history: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


def _update_progress(current: int, total: int, downloaded: int, failed: int):
    """Update download progress state"""
    global download_state
    
    try:
        download_state['current_session'] = current
        download_state['total_sessions'] = total
        download_state['downloaded_count'] = downloaded
        download_state['failed_count'] = failed
        
        # Calculate progress percentage
        if total > 0:
            download_state['progress_percentage'] = (current / total) * 100
        else:
            download_state['progress_percentage'] = 0
        
        # Log progress to console for debugging with timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        logger.info(f"[{timestamp}] [PROGRESS UPDATE] {current}/{total} ({download_state['progress_percentage']:.1f}%) - Downloaded: {downloaded}, Failed: {failed}")
        print(f"[{timestamp}] [ZOOM PROGRESS] {current}/{total} sessions processed ({download_state['progress_percentage']:.1f}%) - Downloaded: {downloaded}, Failed: {failed}")
    except Exception as e:
        logger.error(f"Error updating progress: {e}\n{traceback.format_exc()}")


def _run_download(start_date: str, end_date: str, max_duration_minutes: int):
    """Run the download in background thread"""
    global download_state, download_service
    
    start_time = datetime.now()
    thread_name = threading.current_thread().name
    logger.info(f"[{thread_name}] Zoom download thread started: {start_date} to {end_date}, max_duration={max_duration_minutes}")
    
    try:
        if not download_service:
            error_msg = 'Download service not initialized'
            logger.error(f"[{thread_name}] {error_msg}")
            download_state['error'] = error_msg
            download_state['is_running'] = False
            return
        
        # Run the download with comprehensive error handling
        try:
            download_service.download_chat_messages(
                start_date=start_date,
                end_date=end_date,
                max_duration_minutes=max_duration_minutes,
                progress_callback=_update_progress
            )
            
            logger.info(f"[{thread_name}] download_chat_messages() completed successfully")
            
        except KeyboardInterrupt:
            logger.warning(f"[{thread_name}] Download interrupted by user")
            download_state['error'] = 'Download interrupted by user'
            download_state['is_running'] = False
            return
        except Exception as download_error:
            error_msg = f"Error in download_chat_messages(): {str(download_error)}"
            logger.error(f"[{thread_name}] {error_msg}\n{traceback.format_exc()}")
            download_state['error'] = error_msg
            download_state['is_running'] = False
            download_state['end_time'] = datetime.now()
            
            # Send error notification
            try:
                email_service = EmailService()
                elapsed_time = (datetime.now() - start_time).total_seconds()
                email_service.send_download_completion_notification(
                    to_email="alai@halocollar.com",
                    batch_size=0,  # Not applicable for Zoom
                    downloaded_count=download_state.get('downloaded_count', 0),
                    failed_count=download_state.get('failed_count', 0),
                    elapsed_time_seconds=elapsed_time,
                    date_range=(start_date, end_date),
                    error=error_msg
                )
            except Exception as email_error:
                logger.warning(f"Failed to send error email notification: {email_error}")
            return
        
        # Mark as completed
        download_state['is_running'] = False
        download_state['end_time'] = datetime.now()
        
        # Calculate elapsed time
        elapsed_time = (download_state['end_time'] - start_time).total_seconds()
        
        logger.info(f"[{thread_name}] Download completed successfully in {elapsed_time:.2f} seconds")
        logger.info(f"[{thread_name}] Final stats: downloaded={download_state['downloaded_count']}, "
                   f"failed={download_state['failed_count']}")
        
        # Send email notification
        try:
            email_service = EmailService()
            email_service.send_download_completion_notification(
                to_email="alai@halocollar.com",
                batch_size=0,  # Not applicable for Zoom
                downloaded_count=download_state['downloaded_count'],
                failed_count=download_state['failed_count'],
                elapsed_time_seconds=elapsed_time,
                date_range=(start_date, end_date),
                error=None
            )
            logger.info(f"[{thread_name}] Success notification email sent")
        except Exception as email_error:
            logger.warning(f"[{thread_name}] Failed to send email notification: {email_error}\n{traceback.format_exc()}")
        
    except Exception as e:
        error_msg = f"Unexpected error in download thread: {str(e)}"
        logger.error(f"[{thread_name}] {error_msg}\n{traceback.format_exc()}")
        download_state['error'] = error_msg
        download_state['is_running'] = False
        download_state['end_time'] = datetime.now()
        
        # Calculate elapsed time
        elapsed_time = (download_state['end_time'] - start_time).total_seconds() if download_state['end_time'] else None
        
        # Send email notification for error
        try:
            email_service = EmailService()
            email_service.send_download_completion_notification(
                to_email="alai@halocollar.com",
                batch_size=0,
                downloaded_count=download_state.get('downloaded_count', 0),
                failed_count=download_state.get('failed_count', 0),
                elapsed_time_seconds=elapsed_time,
                date_range=(start_date, end_date),
                error=error_msg
            )
        except Exception as email_error:
            logger.warning(f"[{thread_name}] Failed to send error email notification: {email_error}\n{traceback.format_exc()}")
    finally:
        # Ensure is_running is always set to False when thread exits
        if download_state['is_running']:
            logger.warning(f"[{thread_name}] Thread exiting but is_running was still True, fixing state")
            download_state['is_running'] = False
        logger.info(f"[{thread_name}] Zoom download thread finished")

