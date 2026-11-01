"""
Authentication middleware for protecting API routes
"""

from functools import wraps
from flask import session, jsonify, request
from ...utils.logging import get_logger
from ...services.auth_service import AuthService

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
        
        # Fallback: a signed token issued by /api/auth/password-login
        if AuthService.verify_auth_token(request.headers.get('X-Auth-Token')):
            logger.debug(f"Authenticated via token header for {request.path}")
            return f(*args, **kwargs)
        
        # Not authenticated
        logger.warning(f"Unauthorized access attempt to {request.path}")
        return jsonify({
            'error': 'Authentication required',
            'message': 'Please log in to access this resource'
        }), 401
    
    return decorated_function


def require_admin_auth(f):
    """
    Decorator to require admin authentication for admin API routes
    
    Usage:
        @require_admin_auth
        @some_bp.route('/admin-protected')
        def admin_route():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is authenticated as admin via session
        try:
            if session.get('admin_authenticated', False):
                return f(*args, **kwargs)
        except RuntimeError:
            # Session not available (no secret key) - check for token header
            pass
        
        # Fallback: a signed admin token issued by /api/auth/admin-login
        if AuthService.verify_admin_token(request.headers.get('X-Admin-Token')):
            logger.debug(f"Admin authenticated via token header for {request.path}")
            return f(*args, **kwargs)
        
        # Not authenticated as admin
        logger.warning(f"Unauthorized admin access attempt to {request.path}")
        return jsonify({
            'error': 'Admin authentication required',
            'message': 'Please log in with admin credentials to access this resource'
        }), 401
    
    return decorated_function


LABELING_VIEWER_ROLE = 'labeling_viewer'

# The only API calls a labeling viewer may make: read-only labeling stats and login.
_VIEWER_ALLOWED = {
    ('GET', '/api/labeling/status'),
    ('GET', '/api/labeling/summary'),
    ('GET', '/api/labeling/collar-owners'),
    ('GET', '/api/auth/status'),
    ('GET', '/api/auth/admin-status'),
    ('POST', '/api/auth/logout'),
}


def is_labeling_viewer() -> bool:
    """True when the session belongs to an outside labeling viewer."""
    try:
        return session.get('role') == LABELING_VIEWER_ROLE
    except RuntimeError:
        return False


def restrict_labeling_viewers():
    """
    before_request hook: a labeling viewer gets 403 on every API call outside
    _VIEWER_ALLOWED, whatever decorator (or none) the route has.
    """
    if not request.path.startswith('/api/') or not is_labeling_viewer():
        return None
    if (request.method, request.path.rstrip('/')) in _VIEWER_ALLOWED:
        return None
    if request.method == 'OPTIONS':
        return None
    logger.warning(f"Labeling viewer blocked from {request.method} {request.path}")
    return jsonify({
        'error': 'Not available',
        'message': 'This account can only view labeling stats.'
    }), 403


def require_labeling_read(f):
    """Admins, or a labeling viewer for read-only labeling routes."""
    admin_only = require_admin_auth(f)

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if is_labeling_viewer():
            return f(*args, **kwargs)
        return admin_only(*args, **kwargs)

    return decorated_function
