"""
Analytics middleware for tracking API requests
"""

from flask import request, g, session
from ...utils.logging import get_logger

logger = get_logger('analytics_middleware')


def register_analytics_middleware(app, analytics_service):
    """
    Register analytics tracking middleware
    
    Args:
        app: Flask application instance
        analytics_service: AnalyticsService instance
    """
    
    @app.before_request
    def track_request():
        """Track API requests for analytics"""
        try:
            # Skip tracking for certain paths
            skip_paths = ['/api/health', '/api/analytics/track', '/favicon.ico']
            if any(request.path.startswith(path) for path in skip_paths):
                return
            
            # Only track API routes
            if not request.path.startswith('/api/'):
                return
            
            # Get session ID
            session_id = None
            try:
                if session:
                    # Flask session ID is stored in session cookie
                    # We can use a hash of the session or generate a unique ID
                    session_id = session.get('session_id')
                    if not session_id:
                        # Generate a session ID if not exists
                        import hashlib
                        import secrets
                        session_key = session.get('_permanent_session_lifetime', secrets.token_hex(16))
                        session_id = hashlib.sha256(str(session_key).encode()).hexdigest()[:16]
                        session['session_id'] = session_id
            except Exception as e:
                logger.debug(f"Could not get session ID: {e}")
                # Generate a temporary session ID
                import hashlib
                import secrets
                session_id = hashlib.sha256(secrets.token_hex(16).encode()).hexdigest()[:16]
            
            # Get IP address (check X-Forwarded-For for proxies)
            ip_address = request.headers.get('X-Forwarded-For', '').split(',')[0].strip()
            if not ip_address:
                ip_address = request.remote_addr or 'Unknown'
            
            # Get user agent
            user_agent = request.headers.get('User-Agent', 'Unknown')
            
            # Get referrer
            referrer = request.headers.get('Referer') or request.headers.get('Referrer') or ''
            
            # Get query parameters
            query_params = dict(request.args)
            
            # Get request ID if available
            request_id = g.get('request_id', None)
            
            # Track the event
            event_data = {
                'session_id': session_id,
                'ip_address': ip_address,
                'user_agent': user_agent,
                'page_path': request.path,
                'referrer': referrer,
                'query_params': query_params,
                'request_id': request_id,
                'method': request.method
            }
            
            analytics_service.track_event(event_data)
            
        except Exception as e:
            # Don't let analytics errors break the request
            logger.debug(f"Error tracking analytics: {e}")

