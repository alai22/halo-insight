"""
Authentication Service for Magic Link Authentication
"""

import secrets
import hashlib
import hmac
import time
from datetime import datetime, timedelta
from typing import Optional, Dict
import logging
from backend.core.interfaces import IAuthService
from backend.utils.config import Config

logger = logging.getLogger(__name__)


class AuthService(IAuthService):
    """Service for managing authentication tokens and magic links"""
    
    # In-memory token storage (in production, consider using Redis)
    _tokens: Dict[str, Dict] = {}
    
    # Token expiration time (default 30 minutes)
    TOKEN_EXPIRATION_MINUTES = 30
    
    @classmethod
    def _cleanup_expired_tokens(cls):
        """Remove expired tokens from storage"""
        now = datetime.utcnow()
        expired_tokens = [
            token for token, data in cls._tokens.items()
            if data['expires_at'] < now
        ]
        for token in expired_tokens:
            del cls._tokens[token]
    
    @classmethod
    def validate_email_domain(cls, email: str) -> bool:
        """Validate that email belongs to an allowed domain (Config.ALLOWED_EMAIL_DOMAINS)."""
        if not email or '@' not in email:
            return False
        domain = email.split('@')[1].lower()
        return domain in Config.allowed_email_domains()
    
    @classmethod
    def generate_token(cls, email: str) -> str:
        """
        Generate a secure token for magic link authentication
        
        Args:
            email: User's email address
            
        Returns:
            Secure token string
        """
        # Clean up expired tokens first
        cls._cleanup_expired_tokens()
        
        # Generate cryptographically secure random token
        token = secrets.token_urlsafe(32)
        
        # Store token with expiration
        expires_at = datetime.utcnow() + timedelta(minutes=cls.TOKEN_EXPIRATION_MINUTES)
        cls._tokens[token] = {
            'email': email.lower(),
            'created_at': datetime.utcnow(),
            'expires_at': expires_at,
            'used': False
        }
        
        logger.info(f"Generated magic link token for {email}, expires at {expires_at}")
        return token
    
    @classmethod
    def verify_token(cls, token: str) -> Optional[str]:
        """
        Verify a magic link token and return the associated email
        
        Args:
            token: Token to verify
            
        Returns:
            Email address if token is valid, None otherwise
        """
        # Clean up expired tokens
        cls._cleanup_expired_tokens()
        
        if token not in cls._tokens:
            logger.warning(f"Token not found: {token[:10]}...")
            return None
        
        token_data = cls._tokens[token]
        
        # Check if token is expired
        if datetime.utcnow() > token_data['expires_at']:
            logger.warning(f"Token expired: {token[:10]}...")
            del cls._tokens[token]
            return None
        
        # Check if token was already used
        if token_data['used']:
            logger.warning(f"Token already used: {token[:10]}...")
            return None
        
        # Mark token as used
        token_data['used'] = True
        
        logger.info(f"Token verified successfully for {token_data['email']}")
        return token_data['email']
    
    @classmethod
    def revoke_token(cls, token: str) -> bool:
        """Revoke a token (mark as used)"""
        if token in cls._tokens:
            cls._tokens[token]['used'] = True
            return True
        return False
    
    @classmethod
    def get_token_count(cls) -> int:
        """Get count of active tokens (for monitoring)"""
        cls._cleanup_expired_tokens()
        return len(cls._tokens)

    # Admin header tokens (X-Admin-Token) are stateless and signed, so they work
    # across workers and restarts. Changing ADMIN_PASSWORD revokes them.
    ADMIN_TOKEN_TTL_SECONDS = 12 * 60 * 60

    @staticmethod
    def _admin_token_key() -> Optional[bytes]:
        """Signing key for admin tokens, or None when admin password login is off."""
        if not Config.ADMIN_PASSWORD:
            return None
        material = f"admin-token:{Config.ADMIN_PASSWORD}:{Config.FLASK_SECRET_KEY or ''}"
        return hashlib.sha256(material.encode()).digest()

    @classmethod
    def _sign_admin_expiry(cls, key: bytes, expires_at: int) -> str:
        return hmac.new(key, f"admin:{expires_at}".encode(), hashlib.sha256).hexdigest()

    @classmethod
    def issue_admin_token(cls) -> Optional[str]:
        """Issue a signed admin token of the form '<expires_at>.<signature>'."""
        key = cls._admin_token_key()
        if key is None:
            return None
        expires_at = int(time.time()) + cls.ADMIN_TOKEN_TTL_SECONDS
        return f"{expires_at}.{cls._sign_admin_expiry(key, expires_at)}"

    @classmethod
    def verify_admin_token(cls, token: Optional[str]) -> bool:
        """True only for an unexpired token issued by issue_admin_token."""
        key = cls._admin_token_key()
        if key is None or not token or '.' not in token:
            return False
        expires_part, signature = token.split('.', 1)
        try:
            expires_at = int(expires_part)
        except ValueError:
            return False
        if expires_at < time.time():
            return False
        expected = cls._sign_admin_expiry(key, expires_at)
        return hmac.compare_digest(expected.encode(), signature.encode())
