"""
Error handling middleware with request ID support
"""

from flask import jsonify, request, g
from ...utils.logging import get_logger
from ...core.exceptions import AppException
import traceback

logger = get_logger('error_handlers')


def register_error_handlers(app):
    """Register error handlers for the Flask app with request ID support"""
    
    def get_request_id():
        """Helper to get request ID safely"""
        return getattr(g, 'request_id', 'unknown')
    
    @app.errorhandler(AppException)
    def handle_app_exception(error: AppException):
        """Handle custom application exceptions with standardized format"""
        request_id = get_request_id()
        
        # Log the error with appropriate level based on status code
        if error.status_code >= 500:
            logger.error(f"[ERROR HANDLER] [req:{request_id}] {error.error_code} ({error.status_code}): {error.message} | Path: {request.path}")
            if error.details:
                logger.error(f"[ERROR HANDLER] [req:{request_id}] Error details: {error.details}")
        else:
            logger.warning(f"[ERROR HANDLER] [req:{request_id}] {error.error_code} ({error.status_code}): {error.message} | Path: {request.path}")
        
        # Build standardized error response
        error_dict = error.to_dict()
        error_dict['request_id'] = request_id
        
        response = jsonify({
            'success': False,
            'error': error_dict
        })
        response.headers['X-Request-ID'] = request_id
        return response, error.status_code
    
    @app.errorhandler(400)
    def bad_request(error):
        request_id = get_request_id()
        logger.warning(f"[ERROR HANDLER] [req:{request_id}] Bad request (400): {str(error)} | Path: {request.path}")
        response = jsonify({
            'success': False,
            'error': {
                'code': 'BAD_REQUEST',
                'message': 'Bad request',
                'details': {},
                'request_id': request_id
            }
        })
        response.headers['X-Request-ID'] = request_id
        return response, 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        request_id = get_request_id()
        logger.warning(f"[ERROR HANDLER] [req:{request_id}] Unauthorized (401): {str(error)} | Path: {request.path}")
        response = jsonify({
            'success': False,
            'error': {
                'code': 'UNAUTHORIZED',
                'message': 'Unauthorized',
                'details': {},
                'request_id': request_id
            }
        })
        response.headers['X-Request-ID'] = request_id
        return response, 401
    
    @app.errorhandler(404)
    def not_found(error):
        request_id = get_request_id()
        logger.warning(f"[ERROR HANDLER] [req:{request_id}] Not found (404): {str(error)} | Path: {request.path}")
        response = jsonify({
            'success': False,
            'error': {
                'code': 'NOT_FOUND',
                'message': 'Not found',
                'details': {},
                'request_id': request_id
            }
        })
        response.headers['X-Request-ID'] = request_id
        return response, 404
    
    @app.errorhandler(431)
    def request_header_fields_too_large(error):
        request_id = get_request_id()
        logger.error(f"[ERROR HANDLER] [req:{request_id}] Request Header Fields Too Large (431): {str(error)} | Path: {request.path}")
        logger.error(f"[ERROR HANDLER] [req:{request_id}] Request headers size: {sum(len(k) + len(v) for k, v in request.headers.items())} bytes")
        response = jsonify({
            'success': False,
            'error': {
                'code': 'REQUEST_HEADER_FIELDS_TOO_LARGE',
                'message': 'Request header fields too large',
                'details': {
                    'header_size_bytes': sum(len(k) + len(v) for k, v in request.headers.items()),
                    'suggestion': 'The request headers exceed the maximum size allowed by the server.'
                },
                'request_id': request_id
            }
        })
        response.headers['X-Request-ID'] = request_id
        return response, 431
    
    @app.errorhandler(500)
    def internal_error(error):
        request_id = get_request_id()
        logger.error(f"[ERROR HANDLER] [req:{request_id}] Internal server error (500): {str(error)} | Path: {request.path}")
        logger.error(f"[ERROR HANDLER] [req:{request_id}] Traceback: {traceback.format_exc()}")
        response = jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'Internal server error',
                'details': {},
                'request_id': request_id
            }
        })
        response.headers['X-Request-ID'] = request_id
        return response, 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle all unhandled exceptions - should be last handler"""
        request_id = get_request_id()
        logger.error(f"[ERROR HANDLER] [req:{request_id}] Unhandled exception: {type(error).__name__}: {str(error)} | Path: {request.path}")
        logger.error(f"[ERROR HANDLER] [req:{request_id}] Traceback: {traceback.format_exc()}")
        
        # If it's an AppException that somehow wasn't caught, use its format
        if isinstance(error, AppException):
            return handle_app_exception(error)
        
        response = jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An unexpected error occurred',
                'details': {
                    'error_type': type(error).__name__
                },
                'request_id': request_id
            }
        })
        response.headers['X-Request-ID'] = request_id
        return response, 500
