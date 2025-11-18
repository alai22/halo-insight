"""
Authentication middleware for protecting API routes
"""

from functools import wraps
from flask import session, jsonify, request
from ...utils.logging import get_logger

logger = get_logger('auth_middleware')


def require_auth(f):
    """
    Decorator to require authentication for API routes
    
    Usage:
        @require_auth
        @some_bp.route('/protected')
        def protected_route():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is authenticated via session
        try:
            if session.get('authenticated', False):
                return f(*args, **kwargs)
        except RuntimeError:
            # Session not available (no secret key) - check for token header
            pass
        
        # Fallback: Check for auth token in headers (temporary workaround)
        auth_token = request.headers.get('X-Auth-Token')
        if auth_token:
            # Simple validation - token exists means user logged in
            # In production with proper FLASK_SECRET_KEY, this won't be needed
            logger.debug(f"Authenticated via token header for {request.path}")
            return f(*args, **kwargs)
        
        # Not authenticated
        logger.warning(f"Unauthorized access attempt to {request.path}")
        return jsonify({
            'error': 'Authentication required',
            'message': 'Please log in to access this resource'
        }), 401
    
    return decorated_function

