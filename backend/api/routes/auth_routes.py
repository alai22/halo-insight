"""
API routes for authentication (magic link and Google OAuth)
"""

from flask import Blueprint, request, jsonify, session, redirect, url_for
from ...utils.logging import get_logger
from ...services.auth_service import AuthService
from ...utils.email_service import EmailService
from ...utils.config import Config
from urllib.parse import quote
import os

logger = get_logger('auth_routes')

# Create blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/request-login', methods=['POST'])
def request_login():
    """Request a magic link login"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        
        if not email:
            return jsonify({
                'success': False,
                'error': 'Email is required'
            }), 400
        
        # Validate email domain
        if not AuthService.validate_email_domain(email):
            logger.warning(f"Login attempt from unauthorized domain: {email}")
            # Don't reveal that domain check failed - just say email sent
            # This prevents email enumeration attacks
            return jsonify({
                'success': True,
                'message': 'If this email is registered, you will receive a login link.'
            }), 200
        
        # Generate magic link token
        token = AuthService.generate_token(email)
        
        # Build magic link URL
        # Get base URL from request or environment variable
        base_url = os.getenv('APP_BASE_URL', request.host_url.rstrip('/'))
        # Use /api/auth/verify endpoint which handles both GET and POST
        magic_link = f"{base_url}/api/auth/verify?token={token}"
        
        # Send magic link email
        email_service = EmailService()
        
        if not email_service.is_configured():
            logger.error("Email service not configured - cannot send magic link")
            return jsonify({
                'success': False,
                'error': 'Email service not configured. Please contact administrator.'
            }), 500
        
        # Create email content
        subject = "Your Halo Insight Login Link"
        html_body = f"""
        <html>
          <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #2563eb;">Halo Insight Login</h2>
            <p>Click the button below to log in to Halo Insight:</p>
            <p style="margin: 30px 0;">
              <a href="{magic_link}" 
                 style="background-color: #2563eb; color: white; padding: 12px 24px; 
                        text-decoration: none; border-radius: 6px; display: inline-block; 
                        font-weight: bold;">
                Log In to Halo Insight
              </a>
            </p>
            <p style="color: #666; font-size: 0.9em;">
              This link will expire in 30 minutes.<br>
              If you didn't request this link, you can safely ignore this email.
            </p>
            <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
            <p style="color: #999; font-size: 0.8em;">
              Or copy and paste this link into your browser:<br>
              <a href="{magic_link}" style="color: #2563eb; word-break: break-all;">{magic_link}</a>
            </p>
          </body>
        </html>
        """
        
        text_body = f"""
Halo Insight Login

Click the link below to log in to Halo Insight:

{magic_link}

This link will expire in 30 minutes.
If you didn't request this link, you can safely ignore this email.
        """
        
        # Send email
        success = email_service.send_notification(
            to_email=email,
            subject=subject,
            body=text_body,
            html_body=html_body
        )
        
        if not success:
            logger.error(f"Failed to send magic link email to {email}")
            return jsonify({
                'success': False,
                'error': 'Failed to send login email. Please try again later.'
            }), 500
        
        logger.info(f"Magic link sent successfully to {email}")
        return jsonify({
            'success': True,
            'message': 'Check your email for a login link'
        }), 200
    
    except Exception as e:
        logger.error(f"Error requesting login: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'An error occurred. Please try again later.'
        }), 500


@auth_bp.route('/verify', methods=['GET', 'POST'])
def verify_token():
    """Verify magic link token and create session"""
    try:
        # Get token from query params (GET) or JSON body (POST)
        if request.method == 'GET':
            token = request.args.get('token')
        else:
            data = request.get_json()
            token = data.get('token')
        
        if not token:
            return jsonify({
                'success': False,
                'error': 'Token is required'
            }), 400
        
        # Verify token
        email = AuthService.verify_token(token)
        
        if not email:
            return jsonify({
                'success': False,
                'error': 'Invalid or expired login link. Please request a new one.'
            }), 400
        
        # Create session
        session['authenticated'] = True
        session['email'] = email
        session['auth_method'] = 'magic_link'
        session.permanent = True  # Make session persistent
        
        logger.info(f"User authenticated successfully: {email}")
        
        # Return success response
        # If GET request, redirect to frontend (handled by frontend)
        # If POST request, return JSON
        if request.method == 'POST':
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'email': email
            }), 200
        else:
            # For GET requests, redirect to frontend with success indicator
            # Frontend will handle the redirect
            from flask import redirect
            return redirect(f"/?auth=success&email={email}")
    
    except Exception as e:
        logger.error(f"Error verifying token: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'An error occurred during verification. Please try again.'
        }), 500


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Log out the current user"""
    try:
        session.clear()
        logger.info("User logged out")
        return jsonify({
            'success': True,
            'message': 'Logged out successfully'
        }), 200
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An error occurred during logout'
        }), 500


@auth_bp.route('/status', methods=['GET'])
def auth_status():
    """Check authentication status"""
    try:
        # Try to check session first
        try:
            is_authenticated = session.get('authenticated', False)
            email = session.get('email', None)
            auth_method = session.get('auth_method', None)
            if is_authenticated:
                logger.debug("Authenticated via session")
                return jsonify({
                    'authenticated': True,
                    'email': email,
                    'auth_method': auth_method,
                    'session_available': True
                }), 200
        except RuntimeError as session_error:
            # Session not available - check for token in request headers
            logger.debug(f"Session unavailable, checking token header: {session_error}")
            pass
        
        # Check for auth token in headers (temporary workaround)
        auth_token = request.headers.get('X-Auth-Token')
        if auth_token:
            # Simple validation - token exists means user logged in
            # In production with proper FLASK_SECRET_KEY, this won't be needed
            logger.info(f"Authenticated via token header (token length: {len(auth_token)})")
            return jsonify({
                'authenticated': True,
                'email': None,
                'session_available': False
            }), 200
        
        # Log all headers for debugging
        logger.debug(f"Auth status check - no token found. Headers: {list(request.headers.keys())}")
        logger.debug(f"X-Auth-Token header value: {request.headers.get('X-Auth-Token', 'NOT FOUND')}")
        
        return jsonify({
            'authenticated': False,
            'email': None,
            'session_available': False
        }), 200
    except Exception as e:
        logger.error(f"Error checking auth status: {str(e)}", exc_info=True)
        return jsonify({
            'authenticated': False,
            'email': None,
            'session_available': False
        }), 200


@auth_bp.route('/email-enabled', methods=['GET'])
def check_email_enabled():
    """Check if email service is configured and enabled"""
    try:
        email_service = EmailService()
        is_enabled = email_service.is_configured()
        
        return jsonify({
            'enabled': is_enabled
        }), 200
    except Exception as e:
        logger.error(f"Error checking email service status: {str(e)}")
        return jsonify({
            'enabled': False
        }), 200


@auth_bp.route('/password-login', methods=['POST'])
def password_login():
    """Authenticate using password (backend validation)"""
    try:
        data = request.get_json()
        password = data.get('password', '')
        
        if not password:
            return jsonify({
                'success': False,
                'error': 'Password is required'
            }), 400
        
        # Validate password against backend config
        if password == Config.AUTH_PASSWORD:
            # Try to create session if secret key is available
            try:
                session['authenticated'] = True
                session['auth_method'] = 'password'
                session.permanent = True  # Make session persistent
                logger.info("User authenticated successfully via password (session created)")
            except RuntimeError as session_error:
                # Session creation failed (no secret key) - use token-based auth instead
                logger.warning(f"Session creation failed (likely no FLASK_SECRET_KEY): {session_error}")
                logger.info("Falling back to token-based authentication (temporary workaround)")
                # Return success with a simple token that frontend can store
                # This is a temporary workaround until FLASK_SECRET_KEY is configured
                import hashlib
                import time
                token_data = f"{password}:{time.time()}"
                auth_token = hashlib.sha256(token_data.encode()).hexdigest()[:32]
                
                logger.info("User authenticated successfully via password (token-based, no session)")
                return jsonify({
                    'success': True,
                    'message': 'Login successful',
                    'auth_token': auth_token,  # Frontend will store this
                    'session_available': False  # Indicates session wasn't created
                }), 200
            
            logger.info("User authenticated successfully via password")
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'session_available': True
            }), 200
        else:
            logger.warning("Failed password login attempt")
            return jsonify({
                'success': False,
                'error': 'Incorrect password'
            }), 401
    
    except Exception as e:
        logger.error(f"Error during password login: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'An error occurred during login. Please try again.'
        }), 500


@auth_bp.route('/admin-status', methods=['GET'])
def admin_status():
    """Check admin authentication status"""
    try:
        # Try to check session first
        try:
            is_admin_authenticated = session.get('admin_authenticated', False)
            if is_admin_authenticated:
                logger.debug("Admin authenticated via session")
                return jsonify({
                    'admin_authenticated': True,
                    'session_available': True
                }), 200
        except RuntimeError as session_error:
            # Session not available - check for token in request headers
            logger.debug(f"Session unavailable, checking token header: {session_error}")
            pass
        
        # Check for admin token in headers (temporary workaround)
        admin_token = request.headers.get('X-Admin-Token')
        if admin_token:
            # Simple validation - token exists means admin logged in
            logger.info(f"Admin authenticated via token header (token length: {len(admin_token)})")
            return jsonify({
                'admin_authenticated': True,
                'session_available': False
            }), 200
        
        return jsonify({
            'admin_authenticated': False,
            'session_available': False
        }), 200
    except Exception as e:
        logger.error(f"Error checking admin status: {str(e)}", exc_info=True)
        return jsonify({
            'admin_authenticated': False,
            'session_available': False
        }), 200


@auth_bp.route('/admin-login', methods=['POST'])
def admin_login():
    """Authenticate using admin password (backend validation)"""
    try:
        data = request.get_json()
        password = data.get('password', '')
        
        if not password:
            return jsonify({
                'success': False,
                'error': 'Admin password is required'
            }), 400
        
        # Check if admin password is configured
        if not Config.ADMIN_PASSWORD:
            logger.error("Admin password not configured - admin login disabled")
            return jsonify({
                'success': False,
                'error': 'Admin access is not configured'
            }), 503
        
        # Validate password against admin password
        if password == Config.ADMIN_PASSWORD:
            # Try to create session if secret key is available
            try:
                session['admin_authenticated'] = True
                session['auth_method'] = 'admin_password'
                session.permanent = True  # Make session persistent
                logger.info("Admin authenticated successfully via password (session created)")
            except RuntimeError as session_error:
                # Session creation failed (no secret key) - use token-based auth instead
                logger.warning(f"Session creation failed (likely no FLASK_SECRET_KEY): {session_error}")
                logger.info("Falling back to token-based authentication (temporary workaround)")
                # Return success with a simple token that frontend can store
                import hashlib
                import time
                token_data = f"admin:{password}:{time.time()}"
                admin_token = hashlib.sha256(token_data.encode()).hexdigest()[:32]
                
                logger.info("Admin authenticated successfully via password (token-based, no session)")
                return jsonify({
                    'success': True,
                    'message': 'Admin login successful',
                    'admin_token': admin_token,  # Frontend will store this
                    'session_available': False  # Indicates session wasn't created
                }), 200
            
            logger.info("Admin authenticated successfully via password")
            return jsonify({
                'success': True,
                'message': 'Admin login successful',
                'session_available': True
            }), 200
        else:
            logger.warning("Failed admin password login attempt")
            return jsonify({
                'success': False,
                'error': 'Incorrect admin password'
            }), 401
    
    except Exception as e:
        logger.error(f"Error during admin login: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'An error occurred during admin login. Please try again.'
        }), 500


@auth_bp.route('/google/login', methods=['GET'])
def google_login():
    """Initiate Google OAuth login flow"""
    try:
        # Check if Google OAuth is configured
        if not Config.GOOGLE_OAUTH_CLIENT_ID or not Config.GOOGLE_OAUTH_CLIENT_SECRET:
            logger.error("Google OAuth not configured")
            return jsonify({
                'success': False,
                'error': 'Google SSO is not configured. Please contact administrator.'
            }), 503
        
        # Get redirect URI from config or construct from request
        redirect_uri = Config.GOOGLE_OAUTH_REDIRECT_URI
        if not redirect_uri:
            # Construct from request
            base_url = os.getenv('APP_BASE_URL', request.host_url.rstrip('/'))
            redirect_uri = f"{base_url}/api/auth/google/callback"
        
        # Generate state for CSRF protection
        import secrets
        state = secrets.token_urlsafe(32)
        session['oauth_state'] = state
        
        # Build Google OAuth authorization URL
        from urllib.parse import urlencode
        params = {
            'client_id': Config.GOOGLE_OAUTH_CLIENT_ID,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': 'openid email profile',
            'state': state,
            'access_type': 'offline',
            'prompt': 'select_account'
        }
        
        auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
        
        logger.info(f"Redirecting to Google OAuth")
        return redirect(auth_url)
    
    except Exception as e:
        logger.error(f"Error initiating Google OAuth: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'An error occurred during Google login. Please try again.'
        }), 500


@auth_bp.route('/google/callback', methods=['GET'])
def google_callback():
    """Handle Google OAuth callback"""
    try:
        # Check if Google OAuth is configured
        if not Config.GOOGLE_OAUTH_CLIENT_ID or not Config.GOOGLE_OAUTH_CLIENT_SECRET:
            logger.error("Google OAuth not configured")
            return redirect("/?auth=error&message=Google SSO is not configured")
        
        # Check for error from Google
        error = request.args.get('error')
        if error:
            logger.error(f"Google OAuth error: {error}")
            return redirect("/?auth=error&message=Google authentication was cancelled or failed")
        
        # Verify state (CSRF protection)
        state = request.args.get('state')
        stored_state = session.get('oauth_state')
        if not state or not stored_state or state != stored_state:
            logger.warning("OAuth state mismatch - possible CSRF attack")
            return redirect("/?auth=error&message=Invalid authentication state")
        
        # Clear state from session
        session.pop('oauth_state', None)
        
        # Get authorization code
        code = request.args.get('code')
        if not code:
            logger.error("No authorization code in callback")
            return redirect("/?auth=error&message=No authorization code received")
        
        # Get redirect URI
        redirect_uri = Config.GOOGLE_OAUTH_REDIRECT_URI
        if not redirect_uri:
            base_url = os.getenv('APP_BASE_URL', request.host_url.rstrip('/'))
            redirect_uri = f"{base_url}/api/auth/google/callback"
        
        # Exchange authorization code for access token
        import requests
        token_url = 'https://oauth2.googleapis.com/token'
        token_data = {
            'code': code,
            'client_id': Config.GOOGLE_OAUTH_CLIENT_ID,
            'client_secret': Config.GOOGLE_OAUTH_CLIENT_SECRET,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }
        
        try:
            token_response = requests.post(token_url, data=token_data)
            token_response.raise_for_status()
            token_json = token_response.json()
            access_token = token_json.get('access_token')
            
            if not access_token:
                logger.error("No access token in response")
                return redirect("/?auth=error&message=Failed to obtain access token")
        except Exception as token_error:
            logger.error(f"Error exchanging OAuth code for token: {str(token_error)}")
            return redirect("/?auth=error&message=Failed to authenticate with Google")
        
        # Get user info from Google
        userinfo_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        
        try:
            userinfo_response = requests.get(userinfo_url, headers=headers)
            userinfo_response.raise_for_status()
            user_info = userinfo_response.json()
        except Exception as user_info_error:
            logger.error(f"Error fetching user info from Google: {str(user_info_error)}")
            return redirect("/?auth=error&message=Failed to retrieve user information")
        
        # Extract user information
        email = user_info.get('email', '').lower()
        name = user_info.get('name', '')
        picture = user_info.get('picture', '')
        
        if not email:
            logger.error("No email in Google user info")
            return redirect("/?auth=error&message=No email address found in Google account")
        
        # Validate email domain
        if not AuthService.validate_email_domain(email):
            logger.warning(f"Google OAuth login attempt from unauthorized domain: {email}")
            msg = quote('Your email domain is not allowed to access this application.')
            return redirect(f"/?auth=error&message={msg}")
        
        # Check if user is an admin
        is_admin = Config.is_admin_email(email)
        
        # Create session (same structure as other auth methods)
        session['authenticated'] = True
        session['email'] = email
        session['auth_method'] = 'google'
        if name:
            session['name'] = name
        if picture:
            session['avatar_url'] = picture
        
        # Set admin authentication if email matches admin email(s)
        if is_admin:
            session['admin_authenticated'] = True
            logger.info(f"Admin user authenticated via Google OAuth: {email}")
        else:
            session['admin_authenticated'] = False
        
        session.permanent = True  # Make session persistent
        
        logger.info(f"User authenticated successfully via Google OAuth: {email} (admin: {is_admin})")
        
        # Redirect to frontend with success indicator
        return redirect(f"/?auth=success&email={email}")
    
    except Exception as e:
        logger.error(f"Error in Google OAuth callback: {str(e)}", exc_info=True)
        return redirect("/?auth=error&message=An error occurred during authentication")


@auth_bp.route('/google/enabled', methods=['GET'])
def check_google_enabled():
    """Check if Google OAuth is configured and enabled"""
    try:
        is_enabled = bool(Config.GOOGLE_OAUTH_CLIENT_ID and Config.GOOGLE_OAUTH_CLIENT_SECRET)
        
        return jsonify({
            'enabled': is_enabled
        }), 200
    except Exception as e:
        logger.error(f"Error checking Google OAuth status: {str(e)}")
        return jsonify({
            'enabled': False
        }), 200