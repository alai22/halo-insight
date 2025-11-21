"""
Error handling middleware with request ID support
"""

from flask import jsonify, request, g
from ...utils.logging import get_logger
import traceback

logger = get_logger('error_handlers')


def register_error_handlers(app):
    """Register error handlers for the Flask app with request ID support"""
    
    def get_request_id():
        """Helper to get request ID safely"""
        return getattr(g, 'request_id', 'unknown')
    
    @app.errorhandler(400)
    def bad_request(error):
        request_id = get_request_id()
        logger.warning(f"[ERROR HANDLER] [req:{request_id}] Bad request (400): {str(error)} | Path: {request.path}")
        response = jsonify({'error': 'Bad request', 'status_code': 400, 'request_id': request_id})
        response.headers['X-Request-ID'] = request_id
        return response, 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        request_id = get_request_id()
        logger.warning(f"[ERROR HANDLER] [req:{request_id}] Unauthorized (401): {str(error)} | Path: {request.path}")
        response = jsonify({'error': 'Unauthorized', 'status_code': 401, 'request_id': request_id})
        response.headers['X-Request-ID'] = request_id
        return response, 401
    
    @app.errorhandler(404)
    def not_found(error):
        request_id = get_request_id()
        logger.warning(f"[ERROR HANDLER] [req:{request_id}] Not found (404): {str(error)} | Path: {request.path}")
        response = jsonify({'error': 'Not found', 'status_code': 404, 'request_id': request_id})
        response.headers['X-Request-ID'] = request_id
        return response, 404
    
    @app.errorhandler(431)
    def request_header_fields_too_large(error):
        request_id = get_request_id()
        logger.error(f"[ERROR HANDLER] [req:{request_id}] Request Header Fields Too Large (431): {str(error)} | Path: {request.path}")
        logger.error(f"[ERROR HANDLER] [req:{request_id}] Request headers size: {sum(len(k) + len(v) for k, v in request.headers.items())} bytes")
        response = jsonify({
            'error': 'Request header fields too large', 
            'status_code': 431,
            'request_id': request_id,
            'details': 'The request headers exceed the maximum size allowed by the server.'
        })
        response.headers['X-Request-ID'] = request_id
        return response, 431
    
    @app.errorhandler(500)
    def internal_error(error):
        request_id = get_request_id()
        logger.error(f"[ERROR HANDLER] [req:{request_id}] Internal server error (500): {str(error)} | Path: {request.path}")
        logger.error(f"[ERROR HANDLER] [req:{request_id}] Traceback: {traceback.format_exc()}")
        response = jsonify({'error': 'Internal server error', 'status_code': 500, 'request_id': request_id})
        response.headers['X-Request-ID'] = request_id
        return response, 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        request_id = get_request_id()
        logger.error(f"[ERROR HANDLER] [req:{request_id}] Unhandled exception: {type(error).__name__}: {str(error)} | Path: {request.path}")
        logger.error(f"[ERROR HANDLER] [req:{request_id}] Traceback: {traceback.format_exc()}")
        response = jsonify({
            'error': 'An unexpected error occurred',
            'error_type': type(error).__name__,
            'status_code': 500,
            'request_id': request_id
        })
        response.headers['X-Request-ID'] = request_id
        return response, 500
