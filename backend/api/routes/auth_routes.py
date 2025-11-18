"""
API routes for authentication (magic link)
"""

from flask import Blueprint, request, jsonify, session
from ...utils.logging import get_logger
from ...services.auth_service import AuthService
from ...utils.email_service import EmailService
from ...utils.config import Config
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
        subject = "Your Halo Insights Login Link"
        html_body = f"""
        <html>
          <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #2563eb;">Halo Insights Login</h2>
            <p>Click the button below to log in to Halo Insights:</p>
            <p style="margin: 30px 0;">
              <a href="{magic_link}" 
                 style="background-color: #2563eb; color: white; padding: 12px 24px; 
                        text-decoration: none; border-radius: 6px; display: inline-block; 
                        font-weight: bold;">
                Log In to Halo Insights
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
Halo Insights Login

Click the link below to log in to Halo Insights:

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
        is_authenticated = session.get('authenticated', False)
        email = session.get('email', None)
        
        return jsonify({
            'authenticated': is_authenticated,
            'email': email
        }), 200
    except Exception as e:
        logger.error(f"Error checking auth status: {str(e)}")
        return jsonify({
            'authenticated': False,
            'email': None
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
            # Create session
            session['authenticated'] = True
            session['auth_method'] = 'password'
            session.permanent = True  # Make session persistent
            
            logger.info("User authenticated successfully via password")
            return jsonify({
                'success': True,
                'message': 'Login successful'
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

