"""
Jira API Routes for Bug Triage Copilot

Provides issue list, status, and OAuth 2.0 (3LO) connect flow.
"""

import logging
import secrets
from flask import Blueprint, jsonify, request, redirect, session

from backend.services.jira_client import JiraClient
from backend.services import jira_oauth
from backend.utils.config import Config

logger = logging.getLogger(__name__)

jira_bp = Blueprint('jira', __name__, url_prefix='/api/jira')

# OAuth state key in session
JIRA_OAUTH_STATE_KEY = 'jira_oauth_state'


def _basic_auth_configured() -> bool:
    return bool(Config.JIRA_BASE_URL and Config.JIRA_EMAIL and Config.JIRA_API_TOKEN)


def _oauth_configured() -> bool:
    return bool(
        Config.JIRA_CLIENT_ID and Config.JIRA_CLIENT_SECRET and Config.JIRA_BASE_URL
    )


def _jira_configured() -> bool:
    """True if we can call Jira (Basic auth or OAuth with tokens)."""
    if _basic_auth_configured():
        return True
    if _oauth_configured() and jira_oauth.get_valid_access_token():
        return True
    return False


@jira_bp.route('/status', methods=['GET'])
def get_jira_status():
    """Return whether Jira is configured and how (Basic vs OAuth)."""
    basic = _basic_auth_configured()
    oauth_has_tokens = _oauth_configured() and bool(jira_oauth.get_valid_access_token())
    return jsonify({
        'configured': basic or oauth_has_tokens,
        'base_url': Config.JIRA_BASE_URL or None,
        'auth_type': 'basic' if basic else ('oauth' if oauth_has_tokens else None),
        'oauth_can_connect': _oauth_configured() and bool(Config.APP_BASE_URL),
        'oauth_connected': oauth_has_tokens,
    })


@jira_bp.route('/oauth/authorize', methods=['GET'])
def oauth_authorize():
    """Redirect user to Atlassian to authorize the app. Requires JIRA_CLIENT_ID, JIRA_CLIENT_SECRET, APP_BASE_URL."""
    if not _oauth_configured():
        return jsonify({
            'status': 'error',
            'message': 'Jira OAuth not configured. Set JIRA_CLIENT_ID, JIRA_CLIENT_SECRET, APP_BASE_URL.',
        }), 400
    callback = jira_oauth.get_callback_url(request.url_root.rstrip('/'))
    if not callback:
        return jsonify({
            'status': 'error',
            'message': 'APP_BASE_URL must be set for OAuth callback (e.g. https://insight.halocollar.com).',
        }), 400
    state = secrets.token_urlsafe(24)
    session[JIRA_OAUTH_STATE_KEY] = state
    url = jira_oauth.build_authorize_url(state, request.url_root.rstrip('/'))
    if not url:
        return jsonify({'status': 'error', 'message': 'Could not build authorize URL'}), 400
    return redirect(url)


@jira_bp.route('/oauth/callback', methods=['GET'])
def oauth_callback():
    """Handle redirect from Atlassian: exchange code for tokens, then redirect to frontend."""
    code = request.args.get('code')
    state = request.args.get('state')
    if not code:
        return redirect(_frontend_redirect(error='missing_code'))
    if state != session.get(JIRA_OAUTH_STATE_KEY):
        return redirect(_frontend_redirect(error='invalid_state'))
    session.pop(JIRA_OAUTH_STATE_KEY, None)
    callback = jira_oauth.get_callback_url(request.url_root.rstrip('/'))
    if not callback:
        return redirect(_frontend_redirect(error='no_callback'))
    try:
        result = jira_oauth.exchange_code_for_tokens(code, callback)
        jira_oauth.save_tokens(
            result['access_token'],
            result['refresh_token'],
            result['expires_in'],
        )
        return redirect(_frontend_redirect(connected='1'))
    except Exception as e:
        logger.exception("Jira OAuth token exchange failed: %s", e)
        return redirect(_frontend_redirect(error='exchange_failed'))


@jira_bp.route('/oauth/disconnect', methods=['POST'])
def oauth_disconnect():
    """Clear stored OAuth tokens so user can reconnect or use Basic auth."""
    jira_oauth.clear_tokens()
    return jsonify({'status': 'success', 'message': 'Jira OAuth disconnected'}), 200


def _frontend_redirect(connected: str = None, error: str = None) -> str:
    """Build redirect URL to frontend Jira status view."""
    base = (Config.APP_BASE_URL or '').strip().rstrip('/')
    if not base:
        base = '/'
    path = '/'
    params = ['mode=jira-status']
    if connected:
        params.append('connected=1')
    if error:
        params.append(f'oauth_error={error}')
    return f"{base}{path}?{'&'.join(params)}"


@jira_bp.route('/issues', methods=['GET'])
def get_issues():
    """
    Fetch issues from Jira for Bug Triage. Optional query: project (default HALO), max_results (default 100).
    Uses OAuth if connected, else Basic auth.
    """
    if not _jira_configured():
        return jsonify({
            'status': 'error',
            'message': 'Jira is not connected. Use email + API token in .env, or connect via OAuth (Tools → Jira connection).',
        }), 503

    try:
        project = request.args.get('project', 'HALO').strip() or 'HALO'
        max_results = min(int(request.args.get('max_results', 100)), 100)
        client = JiraClient()
        issues = client.fetch_issues_for_triage(project=project, max_results=max_results)
        return jsonify({
            'status': 'success',
            'data': issues,
            'count': len(issues),
        })
    except ValueError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    except Exception as e:
        logger.exception("Jira fetch failed")
        return jsonify({
            'status': 'error',
            'message': str(e) or 'Failed to fetch issues from Jira',
        }), 500
