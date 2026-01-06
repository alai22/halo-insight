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
from backend.services.zoom_api_client import ZoomAPIClient
from backend.utils.config import Config
from backend.utils.email_service import EmailService
from backend.core.exceptions import ValidationError, ServiceUnavailableError
from backend.utils.error_helpers import validate_date_format, validate_date_range

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
    'progress_percentage': 0,
    'current_phase': None,  # 'fetching_sessions', 'downloading_messages', 'uploading_s3', 'completed'
    'current_session_id': None,
    'total_messages': 0,
    'messages_in_current_session': 0,
    'estimated_time_remaining': None,
    'sessions_per_minute': 0
}

# Global download service instance
download_service: Optional[ZoomDownloadService] = None
download_thread: Optional[threading.Thread] = None


@zoom_bp.route('/download/status', methods=['GET'])
def get_download_status():
    """Get current download status"""
    try:
        # Check if thread is still alive
        thread_alive = download_thread.is_alive() if download_thread else False
        
        # Calculate progress percentage
        if download_state['total_sessions'] > 0:
            download_state['progress_percentage'] = (download_state['current_session'] / download_state['total_sessions']) * 100
        
        # Calculate elapsed time
        elapsed_time = None
        if download_state['start_time']:
            elapsed_time = (datetime.now() - download_state['start_time']).total_seconds()
        
        # Calculate sessions per minute
        sessions_per_minute = 0
        if elapsed_time and elapsed_time > 0 and download_state['current_session'] > 0:
            sessions_per_minute = (download_state['current_session'] / elapsed_time) * 60
        
        # Calculate estimated time remaining
        estimated_time_remaining = None
        if sessions_per_minute > 0 and download_state['total_sessions'] > download_state['current_session']:
            remaining_sessions = download_state['total_sessions'] - download_state['current_session']
            estimated_seconds = (remaining_sessions / sessions_per_minute) * 60
            estimated_time_remaining = estimated_seconds
        
        # If thread is not alive but state says running, mark as error
        if download_state['is_running'] and not thread_alive and not download_state.get('error'):
            logger.warning("Download thread is not alive but state says running - marking as error")
            download_state['is_running'] = False
            download_state['error'] = 'Download thread stopped unexpectedly'
        
        return jsonify({
            'status': 'success',
            'data': {
                'is_running': download_state['is_running'],
                'thread_alive': thread_alive,
                'current_session': download_state['current_session'],
                'total_sessions': download_state['total_sessions'],
                'downloaded_count': download_state['downloaded_count'],
                'failed_count': download_state['failed_count'],
                'progress_percentage': round(download_state['progress_percentage'], 2),
                'start_time': download_state['start_time'].isoformat() if download_state['start_time'] else None,
                'elapsed_time': elapsed_time,
                'error': download_state['error'],
                'current_phase': download_state.get('current_phase'),
                'current_session_id': download_state.get('current_session_id'),
                'total_messages': download_state.get('total_messages', 0),
                'messages_in_current_session': download_state.get('messages_in_current_session', 0),
                'estimated_time_remaining': estimated_time_remaining,
                'sessions_per_minute': round(sessions_per_minute, 2)
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
            raise ValidationError(
                "Download is already running",
                details={'suggestion': 'Wait for the current download to complete or stop it first'}
            )
        
        # Get request data
        data = request.get_json() or {}
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        max_duration_minutes = data.get('max_duration_minutes', 30)
        
        logger.info(f"Starting Zoom download request: start_date={start_date}, end_date={end_date}, "
                   f"max_duration={max_duration_minutes}")
        
        # Validate date parameters
        if not start_date or not end_date:
            raise ValidationError(
                "start_date and end_date are required",
                details={'fields': ['start_date', 'end_date'], 'suggestion': 'Provide both dates in YYYY-MM-DD format'}
            )
        
        # Validate date formats and range
        validate_date_format(start_date, 'start_date')
        validate_date_format(end_date, 'end_date')
        validate_date_range(start_date, end_date)
        
        # Initialize download service
        try:
            logger.info("Initializing ZoomDownloadService...")
            download_service = ZoomDownloadService()
            logger.info("Zoom download service initialized successfully")
        except Exception as e:
            error_msg = f"Failed to initialize download service: {str(e)}"
            logger.error(f"{error_msg}\n{traceback.format_exc()}")
            download_state['is_running'] = False
            download_state['error'] = error_msg
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
            'progress_percentage': 0,
            'current_phase': 'fetching_sessions',
            'current_session_id': None,
            'total_messages': 0,
            'messages_in_current_session': 0,
            'estimated_time_remaining': None,
            'sessions_per_minute': 0
        })
        
        # Start download in background thread
        logger.info(f"Creating download thread for {start_date} to {end_date}")
        download_thread = threading.Thread(
            target=_run_download,
            args=(start_date, end_date, max_duration_minutes),
            daemon=True,
            name="ZoomDownloadThread"
        )
        download_thread.start()
        logger.info(f"Download thread started (thread ID: {download_thread.ident}, name: {download_thread.name})")
        
        # Give thread a moment to start and log
        import time
        time.sleep(0.5)
        
        # Verify thread is alive
        if not download_thread.is_alive():
            logger.warning("Download thread died immediately after starting!")
            download_state['is_running'] = False
            download_state['error'] = 'Download thread failed to start'
            return jsonify({'status': 'error', 'message': 'Download thread failed to start'}), 500
        
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
            raise ValidationError(
                "No download is currently running",
                details={'suggestion': 'Start a download first'}
            )
        
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
    global download_service
    
    try:
        if not download_service:
            try:
                download_service = ZoomDownloadService()
            except Exception as e:
                logger.error(f"Failed to initialize ZoomDownloadService: {e}")
                return jsonify({
                    'status': 'error', 
                    'message': f'Failed to initialize Zoom service: {str(e)}. Please check your Zoom credentials.'
                }), 500
        
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
    global download_service
    
    try:
        if not download_service:
            try:
                download_service = ZoomDownloadService()
            except Exception as e:
                logger.error(f"Failed to initialize ZoomDownloadService: {e}")
                return jsonify({
                    'status': 'error', 
                    'message': f'Failed to initialize Zoom service: {str(e)}. Please check your Zoom credentials.'
                }), 500
        
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


@zoom_bp.route('/status', methods=['GET'])
def get_zoom_status():
    """Get Zoom API credentials status (without exposing actual values)"""
    try:
        from backend.utils.config import Config
        
        # Check if credentials are configured (without exposing values)
        account_id_configured = bool(Config.ZOOM_ACCOUNT_ID and Config.ZOOM_ACCOUNT_ID.strip())
        client_id_configured = bool(Config.ZOOM_CLIENT_ID and Config.ZOOM_CLIENT_ID.strip())
        client_secret_configured = bool(Config.ZOOM_CLIENT_SECRET and Config.ZOOM_CLIENT_SECRET.strip())
        
        all_configured = account_id_configured and client_id_configured and client_secret_configured
        
        # Try to initialize the service to verify credentials work
        credentials_valid = False
        error_message = None
        
        if all_configured:
            try:
                test_client = ZoomAPIClient()
                # Try to get a token (this will fail if credentials are invalid)
                test_client.get_access_token()
                credentials_valid = True
            except Exception as e:
                error_message = str(e)
                logger.warning(f"Zoom credentials check failed: {e}")
                # Try to extract more details from the error if it's an HTTPError
                if hasattr(e, 'response') and e.response is not None:
                    try:
                        error_json = e.response.json()
                        detailed_error = error_json.get('error_description', error_json.get('error', error_message))
                        if detailed_error != error_message:
                            error_message = f"{error_message} - {detailed_error}"
                    except:
                        # If response is not JSON, use the text
                        if e.response.text:
                            error_message = f"{error_message} - {e.response.text[:200]}"
        
        return jsonify({
            'status': 'success',
            'data': {
                'configured': all_configured,
                'credentials_valid': credentials_valid,
                'account_id_configured': account_id_configured,
                'client_id_configured': client_id_configured,
                'client_secret_configured': client_secret_configured,
                'error': error_message
            }
        })
        
    except Exception as e:
        logger.error(f"Error checking Zoom status: {e}")
        return jsonify({
            'status': 'success',
            'data': {
                'configured': False,
                'credentials_valid': False,
                'account_id_configured': False,
                'client_id_configured': False,
                'client_secret_configured': False,
                'error': str(e)
            }
        }), 200


def _update_progress(current: int, total: int, downloaded: int, failed: int, 
                     current_session_id: str = None, messages_in_session: int = 0,
                     total_messages: int = 0, phase: str = None):
    """Update download progress state"""
    global download_state
    
    try:
        download_state['current_session'] = current
        download_state['total_sessions'] = total
        download_state['downloaded_count'] = downloaded
        download_state['failed_count'] = failed
        
        if current_session_id:
            download_state['current_session_id'] = current_session_id
        if messages_in_session > 0:
            download_state['messages_in_current_session'] = messages_in_session
        if total_messages > 0:
            download_state['total_messages'] = total_messages
        if phase:
            download_state['current_phase'] = phase
        
        # Calculate progress percentage
        if total > 0:
            download_state['progress_percentage'] = (current / total) * 100
        else:
            download_state['progress_percentage'] = 0
        
        # Calculate sessions per minute
        if download_state['start_time']:
            elapsed = (datetime.now() - download_state['start_time']).total_seconds()
            if elapsed > 0 and current > 0:
                download_state['sessions_per_minute'] = (current / elapsed) * 60
        
        # Log progress to console for debugging with timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        phase_str = f" [{phase}]" if phase else ""
        session_info = f" (Session: {current_session_id[:20]}...)" if current_session_id else ""
        messages_info = f" | Messages: {messages_in_session} in session, {total_messages} total" if messages_in_session > 0 else ""
        logger.info(f"[{timestamp}] [PROGRESS UPDATE]{phase_str} {current}/{total} ({download_state['progress_percentage']:.1f}%) - Downloaded: {downloaded}, Failed: {failed}{session_info}{messages_info}")
        print(f"[{timestamp}] [ZOOM PROGRESS]{phase_str} {current}/{total} sessions ({download_state['progress_percentage']:.1f}%) - Downloaded: {downloaded}, Failed: {failed}{session_info}{messages_info}")
    except Exception as e:
        logger.error(f"Error updating progress: {e}\n{traceback.format_exc()}")


def _run_download(start_date: str, end_date: str, max_duration_minutes: int):
    """Run the download in background thread"""
    global download_state, download_service
    
    start_time = datetime.now()
    thread_name = threading.current_thread().name
    thread_id = threading.current_thread().ident
    
    logger.info(f"[{thread_name}] ===== Zoom download thread STARTED =====")
    logger.info(f"[{thread_name}] Thread ID: {thread_id}")
    logger.info(f"[{thread_name}] Date range: {start_date} to {end_date}")
    logger.info(f"[{thread_name}] Max duration: {max_duration_minutes} minutes")
    logger.info(f"[{thread_name}] Download service exists: {download_service is not None}")
    
    try:
        if not download_service:
            logger.error(f"[{thread_name}] Download service is None, initializing...")
            try:
                download_service = ZoomDownloadService()
                logger.info(f"[{thread_name}] Successfully initialized download service in thread")
            except Exception as init_error:
                error_msg = f'Failed to initialize download service: {str(init_error)}'
                logger.error(f"[{thread_name}] {error_msg}\n{traceback.format_exc()}")
                download_state['error'] = error_msg
                download_state['is_running'] = False
                return
        
        # Run the download with comprehensive error handling
        try:
            logger.info(f"[{thread_name}] Calling download_service.download_chat_messages()...")
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

