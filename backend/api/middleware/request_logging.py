"""
Request logging middleware with request ID support
"""

from flask import request, g, Response
from ...utils.logging import get_logger
import time
import uuid

logger = get_logger('request_logging')


def register_request_logging(app):
    """Register request logging middleware with request ID support"""
    
    @app.before_request
    def generate_request_id():
        """Generate or extract request ID for distributed tracing"""
        # Check if client sent a request ID (for distributed tracing)
        incoming_id = request.headers.get('X-Request-ID')
        
        if incoming_id:
            # Use client's request ID (for distributed systems)
            g.request_id = incoming_id
            g.request_id_source = 'client'
        else:
            # Generate new UUID (use first 8 chars for readability in logs)
            full_uuid = str(uuid.uuid4())
            g.request_id = full_uuid[:8]  # Short ID for logs (e.g., "a3f8b2c1")
            g.request_id_full = full_uuid  # Full UUID for internal use
            g.request_id_source = 'generated'
        
        # Store request start time for duration calculation
        g.request_start_time = time.time()
    
    @app.before_request
    def log_request():
        """Log incoming requests - only log non-GET requests and errors"""
        request_id = g.get('request_id', 'unknown')
        
        # Calculate total header size
        header_size = sum(len(k) + len(v) + 4 for k, v in request.headers.items())  # +4 for ': ' and '\r\n'
        
        # Only log non-GET requests (POST, PUT, DELETE, etc.) to reduce noise
        # GET requests are logged at debug level, errors are always logged
        if request.method != 'GET':
            logger.info(
                f"[REQUEST] [req:{request_id}] {request.method} {request.path} | "
                f"Remote: {request.remote_addr}"
            )
        else:
            logger.debug(
                f"[REQUEST] [req:{request_id}] {request.method} {request.path} | "
                f"Remote: {request.remote_addr}"
            )
        
        # Log if headers are large (potential 431 issue) - always log warnings
        if header_size > 8000:
            logger.warning(
                f"[REQUEST] [req:{request_id}] Large headers detected: {header_size} bytes | "
                f"Path: {request.path} | "
                f"Cookie header length: {len(request.headers.get('Cookie', ''))}"
            )
        
        # Log headers if verbose (but truncate to avoid huge logs)
        if request.headers:
            header_summary = {k: (v[:100] if len(v) > 100 else v) 
                            for k, v in request.headers.items() 
                            if k.lower() not in ['authorization']}  # Still log cookies to debug 431
            # For cookies, just show length
            if 'Cookie' in request.headers:
                cookie_len = len(request.headers['Cookie'])
                header_summary['Cookie'] = f'[Length: {cookie_len} bytes - truncated for logging]'
            logger.debug(f"[REQUEST] [req:{request_id}] Headers: {header_summary}")
        
        # Log request body for POST/PUT (truncated)
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                if request.is_json:
                    data = request.get_json(silent=True) or {}
                    # Truncate large data
                    data_str = str(data)
                    if len(data_str) > 500:
                        data_str = data_str[:500] + "... (truncated)"
                    logger.debug(f"[REQUEST] [req:{request_id}] JSON body: {data_str}")
                else:
                    body = request.get_data(as_text=True)
                    if body and len(body) > 500:
                        body = body[:500] + "... (truncated)"
                    logger.debug(f"[REQUEST] [req:{request_id}] Body: {body[:500] if body else 'empty'}")
            except Exception as e:
                logger.warning(f"[REQUEST] [req:{request_id}] Failed to log request body: {str(e)}")
    
    @app.after_request
    def add_request_id_header(response):
        """Add request ID to response headers for client tracing"""
        if hasattr(g, 'request_id'):
            response.headers['X-Request-ID'] = g.request_id
        return response
    
    @app.after_request
    def log_response(response):
        """Log outgoing responses - only log errors and non-GET requests"""
        duration = time.time() - g.get('request_start_time', time.time())
        request_id = g.get('request_id', 'unknown')
        
        # Add request ID to response headers (done in separate decorator above)
        
        # Only log non-GET requests or slow requests (>1s) at info level
        # Errors are always logged
        if response.status_code >= 400:
            # Errors are logged below
            pass
        elif request.method != 'GET' or duration > 1.0:
            logger.info(
                f"[RESPONSE] [req:{request_id}] {request.method} {request.path} | "
                f"Status: {response.status_code} | "
                f"Duration: {duration:.3f}s"
            )
        else:
            logger.debug(
                f"[RESPONSE] [req:{request_id}] {request.method} {request.path} | "
                f"Status: {response.status_code} | "
                f"Duration: {duration:.3f}s"
            )
        
        # Log response body for errors (truncated)
        # Skip error logging for common static asset requests (browsers request these automatically)
        common_static_assets = ['/favicon.ico', '/robots.txt', '/apple-touch-icon.png', '/manifest.json']
        is_common_static = request.path in common_static_assets
        
        if response.status_code >= 400:
            try:
                response_data = response.get_data(as_text=True)
                if response_data and len(response_data) > 1000:
                    response_data = response_data[:1000] + "... (truncated)"
                
                # For 404s on common static assets, use debug level instead of error
                if response.status_code == 404 and is_common_static:
                    logger.debug(
                        f"[RESPONSE] [req:{request_id}] {request.method} {request.path} | "
                        f"Status: {response.status_code} | "
                        f"(Common static asset - not an error)"
                    )
                else:
                    logger.error(
                        f"[RESPONSE ERROR] [req:{request_id}] {request.method} {request.path} | "
                        f"Status: {response.status_code} | "
                        f"Body: {response_data}"
                    )
            except Exception as e:
                logger.warning(f"[RESPONSE] [req:{request_id}] Failed to log error response: {str(e)}")
        
        return response

