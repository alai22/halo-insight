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
        # Check if user is authenticated
        if not session.get('authenticated', False):
            logger.warning(f"Unauthorized access attempt to {request.path}")
            return jsonify({
                'error': 'Authentication required',
                'message': 'Please log in to access this resource'
            }), 401
        
        return f(*args, **kwargs)
    
    return decorated_function

