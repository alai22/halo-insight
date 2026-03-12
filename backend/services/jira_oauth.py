"""
Jira OAuth 2.0 (3LO) token storage and refresh.

Atlassian uses rotating refresh tokens: each refresh returns a new refresh_token
that must be stored; the previous one is invalidated.
"""

import json
import os
import time
import logging
from pathlib import Path
from typing import Optional, Dict, Any

import requests

from backend.utils.config import Config
from backend.utils.logging import get_logger

logger = get_logger('jira_oauth')

# Atlassian OAuth endpoints
AUTH_URL = 'https://auth.atlassian.com/authorize'
TOKEN_URL = 'https://auth.atlassian.com/oauth/token'
# Scopes: read Jira issues; offline_access for refresh token
DEFAULT_SCOPES = 'read:jira-work read:jira-user offline_access'


def _tokens_path() -> Path:
    path = Path(Config.JIRA_OAUTH_TOKENS_FILE)
    if not path.is_absolute():
        # Resolve relative to project root (cwd when app runs)
        base = Path.cwd()
        path = base / path
    return path


def load_tokens() -> Optional[Dict[str, Any]]:
    """Load stored tokens from file. Returns None if missing or invalid."""
    path = _tokens_path()
    if not path.exists():
        return None
    try:
        with open(path, 'r') as f:
            data = json.load(f)
        if not data.get('refresh_token'):
            return None
        return data
    except Exception as e:
        logger.warning("Failed to load Jira OAuth tokens: %s", e)
        return None


def save_tokens(access_token: str, refresh_token: str, expires_in: int) -> None:
    """Save tokens to file. expires_in is seconds from now."""
    path = _tokens_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    expires_at = time.time() + expires_in
    data = {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'expires_at': expires_at,
    }
    with open(path, 'w') as f:
        json.dump(data, f, indent=0)
    logger.info("Saved Jira OAuth tokens to %s", path)


def clear_tokens() -> None:
    """Remove stored tokens file."""
    path = _tokens_path()
    if path.exists():
        path.unlink()
        logger.info("Cleared Jira OAuth tokens")


def get_callback_url(request_base_url: Optional[str] = None) -> str:
    """Build the OAuth callback URL. Uses APP_BASE_URL or request base URL."""
    base = (Config.APP_BASE_URL or '').strip().rstrip('/')
    if not base and request_base_url:
        base = request_base_url.rstrip('/')
    if not base:
        return ''
    return f"{base}/api/jira/oauth/callback"


def build_authorize_url(state: str, request_base_url: Optional[str] = None) -> Optional[str]:
    """Build Atlassian authorization URL. Returns None if client_id or callback not configured."""
    client_id = (Config.JIRA_CLIENT_ID or '').strip()
    callback = get_callback_url(request_base_url)
    if not client_id or not callback:
        return None
    params = {
        'client_id': client_id,
        'scope': DEFAULT_SCOPES,
        'redirect_uri': callback,
        'state': state,
        'response_type': 'code',
        'prompt': 'consent',
    }
    qs = '&'.join(f"{k}={requests.utils.quote(str(v))}" for k, v in params.items())
    return f"{AUTH_URL}?{qs}"


def exchange_code_for_tokens(code: str, redirect_uri: str) -> Dict[str, Any]:
    """
    Exchange authorization code for access and refresh tokens.
    Returns dict with access_token, refresh_token, expires_in.
    Raises on HTTP or API error.
    """
    client_id = (Config.JIRA_CLIENT_ID or '').strip()
    client_secret = (Config.JIRA_CLIENT_SECRET or '').strip()
    if not client_id or not client_secret:
        raise ValueError("JIRA_CLIENT_ID and JIRA_CLIENT_SECRET must be set")
    resp = requests.post(
        TOKEN_URL,
        json={
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'redirect_uri': redirect_uri,
        },
        headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    access = data.get('access_token')
    refresh = data.get('refresh_token')
    expires_in = int(data.get('expires_in', 3600))
    if not access or not refresh:
        raise ValueError("Token response missing access_token or refresh_token")
    return {'access_token': access, 'refresh_token': refresh, 'expires_in': expires_in}


def refresh_access_token() -> Optional[str]:
    """
    Use stored refresh token to get a new access token. Saves new tokens (rotating refresh).
    Returns new access_token or None on failure.
    """
    tokens = load_tokens()
    if not tokens:
        return None
    refresh_token = tokens.get('refresh_token')
    if not refresh_token:
        return None
    client_id = (Config.JIRA_CLIENT_ID or '').strip()
    client_secret = (Config.JIRA_CLIENT_SECRET or '').strip()
    if not client_id or not client_secret:
        return None
    resp = requests.post(
        TOKEN_URL,
        json={
            'grant_type': 'refresh_token',
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token,
        },
        headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
        timeout=30,
    )
    if resp.status_code != 200:
        logger.warning("Jira OAuth refresh failed: %s %s", resp.status_code, resp.text)
        return None
    data = resp.json()
    access = data.get('access_token')
    new_refresh = data.get('refresh_token', refresh_token)
    expires_in = int(data.get('expires_in', 3600))
    if access:
        save_tokens(access, new_refresh, expires_in)
    return access


def get_valid_access_token() -> Optional[str]:
    """
    Return a valid access token: from store if not expired, else refresh.
    Returns None if no tokens or refresh fails.
    """
    tokens = load_tokens()
    if not tokens:
        return None
    access = tokens.get('access_token')
    expires_at = tokens.get('expires_at', 0)
    # Consider expired 60s early to avoid race
    if access and expires_at and time.time() < expires_at - 60:
        return access
    return refresh_access_token()
