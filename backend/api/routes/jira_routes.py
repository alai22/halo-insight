"""
Jira API Routes for Bug Triage Copilot

Provides issue list, status, OAuth 2.0 (3LO) connect flow, and AI backlog overview.
"""

import logging
import secrets
from typing import Any, Dict, List, Optional

from flask import Blueprint, g, jsonify, redirect, request, session
import requests

from backend.services.jira_client import JiraClient
from backend.services import jira_oauth
from backend.utils.config import Config
from backend.utils.pii_protection import create_pii_protector

logger = logging.getLogger(__name__)

# Max chars of response body to include in error_details (avoid huge payloads)
JIRA_ERROR_SNIPPET_MAX = 800


def _jira_http_error_response(e: requests.HTTPError, fallback_message: str):
    """Build (message, error_details, status_code) from a requests HTTPError for Jira API."""
    status_code = e.response.status_code if e.response is not None else 500
    message_parts = [f"Jira returned {status_code}"]
    response_snippet = None
    try:
        if e.response is not None and e.response.text:
            response_snippet = (e.response.text or "")[:JIRA_ERROR_SNIPPET_MAX]
            if e.response.headers.get("content-type", "").startswith("application/json"):
                body = e.response.json()
                if isinstance(body, dict):
                    if body.get("errorMessages"):
                        message_parts.append("; ".join(body["errorMessages"]))
                    if body.get("errors") and isinstance(body["errors"], dict):
                        for k, v in body["errors"].items():
                            message_parts.append(f"{k}: {v}")
                    elif body.get("errors"):
                        message_parts.append(str(body["errors"]))
    except Exception:
        pass
    message = " — ".join(message_parts) if len(message_parts) > 1 else (message_parts[0] if message_parts else fallback_message)
    error_details = {"status_code": status_code}
    if response_snippet:
        error_details["response_snippet"] = response_snippet
    return message, error_details, min(status_code, 599)

jira_bp = Blueprint('jira', __name__, url_prefix='/api/jira')

# OAuth state key in session
JIRA_OAUTH_STATE_KEY = 'jira_oauth_state'

# POST /backlog-overview: allowed issue keys from client; max issues and title length for prompt size
_OVERVIEW_ALLOWED_KEYS = frozenset({
    'key', 'title', 'priority', 'status', 'issuetype', 'component', 'components', 'labels',
    'parentKey', 'parentSummary', 'epicKey', 'epicSummary', 'sprint', 'gaBlocker', 'needsMoreInfo',
})
_OVERVIEW_MAX_ISSUES = 450
_OVERVIEW_MAX_TITLE_LEN = 240
_OVERVIEW_MAX_LABELS = 20
_OVERVIEW_MAX_COMPONENTS = 15

_BACKLOG_OVERVIEW_SYSTEM = """You are an engineering lead helping triage a Jira bug backlog for **Halo Collar** (pet GPS / smart collar; mobile apps for pet tracking, maps, geofences, device pairing, etc.). You receive a table of issues (key, title, and metadata only—no full descriptions).

Write a concise markdown overview for the team. Use these sections (omit a section if nothing substantive to say):
## Critical / high-risk themes
## Priority review
Issues that may be mis-prioritized vs severity/labels; suggest re-ordering only when justified by the data.
For each such ticket, **explicitly state whether you recommend escalating** (raising attention/priority) **or de-escalating** (lowering relative priority)—do not leave it ambiguous.
## Needs clarification
Tickets that look vague, blocked, or missing context based on titles/metadata.
## Duplicates or related clusters
Use **two subheadings** when this section has content (omit empty subheadings):
### Likely duplicate candidates
Only when titles/metadata strongly suggest the **same user-visible bug** or **same root cause** (e.g. duplicate report of the identical failure). State briefly why. Cite keys.
### Shared root-cause investigation (optional)
Only when you believe **one fix or one investigation thread** could reasonably address **multiple keys** together—not merely that they touch the same screen family. Name the **hypothesized shared cause** in one short phrase. Cite keys.

**Product context:** Map UI, pet pins, follow mode, pet card, multi-pet map behavior, geofences/fences, and collar/API updates are **different flows** in this product. **Do not** cluster tickets together only because they share platform (iOS/Android), or keywords like map, location, GPS, or pet—surface overlap is normal, not evidence of duplication.

## Other notes
Non-obvious risks or cross-cutting patterns only. Omit this section entirely if everything important is already covered above.

Rules:
- Cite issue keys (e.g. PROJ-123) when you reference specific tickets.
- When you suggest changing how a ticket should be prioritized, label the direction: **Escalate** or **De-escalate**, with a short reason tied to metadata (e.g. labels, GA-blocker flag, priority vs apparent severity).
- Do not invent facts; only infer from the provided list.
- **Duplicates / clusters:** Prefer **no entry** in this section over weak grouping. If you are unsure, omit or mention uncertainty briefly rather than listing loosely related tickets.
- **No filler or throat-clearing.** Do not state the obvious: e.g. that the backlog is large, spans many areas, or covers iOS/Android/platforms, unless you immediately tie it to a **specific triage implication** with cited keys. Readers already see the table; every sentence should add non-obvious or actionable insight.
- Do not open with generic scene-setting. Prefer leading with concrete findings, or one short clause if the filtered set is unremarkable.
- If the list is small or homogeneous, say so in one brief clause—do not pad.
- Keep total length readable (roughly under 800 words)."""


def _sanitize_overview_issue(raw: Any) -> Optional[Dict[str, Any]]:
    """Keep only allowed keys with safe primitive/list values."""
    if not isinstance(raw, dict):
        return None
    key = raw.get('key')
    if not key or not isinstance(key, str):
        return None
    key = key.strip()[:32]
    if not key:
        return None
    out: Dict[str, Any] = {'key': key}
    title = raw.get('title')
    if isinstance(title, str):
        t = title.strip()
        if t:
            out['title'] = t[:_OVERVIEW_MAX_TITLE_LEN]

    def _str_field(name: str, max_len: int = 120):
        v = raw.get(name)
        if isinstance(v, str) and v.strip():
            out[name] = v.strip()[:max_len]

    for name in ('priority', 'status', 'issuetype', 'component', 'parentKey', 'parentSummary', 'epicKey', 'epicSummary', 'sprint'):
        if name in _OVERVIEW_ALLOWED_KEYS:
            _str_field(name, 200 if name in ('parentSummary', 'epicSummary') else 80)

    labels = raw.get('labels')
    if isinstance(labels, list):
        cleaned = []
        for x in labels[:_OVERVIEW_MAX_LABELS]:
            if isinstance(x, str) and x.strip():
                cleaned.append(x.strip()[:80])
        if cleaned:
            out['labels'] = cleaned

    components = raw.get('components')
    if isinstance(components, list):
        cleaned = []
        for x in components[:_OVERVIEW_MAX_COMPONENTS]:
            if isinstance(x, str) and x.strip():
                cleaned.append(x.strip()[:80])
        if cleaned:
            out['components'] = cleaned

    if raw.get('gaBlocker') is True:
        out['gaBlocker'] = True
    if raw.get('needsMoreInfo') is True:
        out['needsMoreInfo'] = True

    return out


def _format_issues_for_overview_prompt(issues: List[Dict[str, Any]], truncated: bool, total_submitted: int) -> str:
    """Build user message text for Claude."""
    lines = [
        f"The following {len(issues)} issues are the current filtered backlog (metadata only).",
    ]
    if truncated:
        lines.append(f"Note: Analyzing first {len(issues)} of {total_submitted} issues submitted (cap for context size).")
    lines.append('')
    lines.append('key | title | type | priority | status | component(s) | labels | parent | epic | flags')
    for i in issues:
        comps = i.get('components') or ([] if not i.get('component') else [i['component']])
        comp_s = ','.join(comps) if comps else ''
        labels = ','.join(i.get('labels') or [])
        flags = []
        if i.get('gaBlocker'):
            flags.append('GA-blocker')
        if i.get('needsMoreInfo'):
            flags.append('needs-info')
        flag_s = ','.join(flags)
        parent = i.get('parentKey') or ''
        if i.get('parentSummary'):
            parent = f"{parent} ({i['parentSummary'][:60]})" if parent else i['parentSummary'][:60]
        epic = i.get('epicKey') or ''
        if i.get('epicSummary'):
            epic = f"{epic} ({i['epicSummary'][:40]})" if epic else i['epicSummary'][:40]
        title = (i.get('title') or '').replace('|', '/').replace('\n', ' ')
        lines.append(
            f"{i['key']} | {title} | {i.get('issuetype') or ''} | {i.get('priority') or ''} | {i.get('status') or ''} | "
            f"{comp_s} | {labels} | {parent} | {epic} | {flag_s}"
        )
    lines.append('')
    lines.append('Produce the markdown overview as instructed.')
    return '\n'.join(lines)


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
    """Return whether Jira is configured and how (Basic preferred over OAuth when both set)."""
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


@jira_bp.route('/projects', methods=['GET'])
def get_projects():
    """
    List projects visible to the configured Jira user (API token or OAuth).
    Use this to verify access and see exact project keys (e.g. for Bug Triage).
    """
    if not _jira_configured():
        return jsonify({
            'status': 'error',
            'message': 'Jira is not connected. Configure Basic auth or OAuth first.',
        }), 503

    try:
        client = JiraClient()
        projects = client.get_projects()
        # Normalize to list of { id, key, name }
        out = []
        for p in projects:
            out.append({
                'id': p.get('id'),
                'key': p.get('key'),
                'name': p.get('name'),
            })
        return jsonify({
            'status': 'success',
            'data': out,
            'count': len(out),
        })
    except requests.exceptions.HTTPError as e:
        logger.warning("Jira projects HTTP error: %s %s", e.response.status_code if e.response else None, getattr(e.response, 'text', '')[:200])
        message, error_details, status_code = _jira_http_error_response(e, 'Failed to fetch projects from Jira')
        return jsonify({
            'status': 'error',
            'message': message,
            'error_details': error_details,
        }), status_code if 400 <= status_code < 600 else 500
    except Exception as e:
        logger.exception("Jira projects fetch failed")
        return jsonify({
            'status': 'error',
            'message': str(e) or 'Failed to fetch projects from Jira',
        }), 500


@jira_bp.route('/myself', methods=['GET'])
def get_myself():
    """Return current Jira user (validates auth)."""
    if not _jira_configured():
        return jsonify({
            'status': 'error',
            'message': 'Jira is not connected.',
        }), 503

    try:
        client = JiraClient()
        me = client.get_myself()
        return jsonify({
            'status': 'success',
            'data': {
                'accountId': me.get('accountId'),
                'displayName': me.get('displayName'),
                'emailAddress': me.get('emailAddress'),
            },
        })
    except requests.exceptions.HTTPError as e:
        logger.warning("Jira myself HTTP error: %s %s", e.response.status_code if e.response else None, getattr(e.response, 'text', '')[:200])
        message, error_details, status_code = _jira_http_error_response(e, 'Failed to get current user from Jira')
        return jsonify({
            'status': 'error',
            'message': message,
            'error_details': error_details,
        }), status_code if 400 <= status_code < 600 else 500
    except Exception as e:
        logger.exception("Jira myself fetch failed")
        return jsonify({
            'status': 'error',
            'message': str(e) or 'Failed to get current user from Jira',
        }), 500


@jira_bp.route('/issues', methods=['GET'])
def get_issues():
    """
    Fetch issues from Jira for Bug Triage. Optional query: project (default HALO), max_results (1–1000, default 1000),
    ancestor_key (e.g. HALO-23306) to restrict to that issue and its descendants (children, grandchildren, etc.),
    issuetype (default Bug) to filter by issue type; use issuetype= or issuetype=all for all types.
    Uses Basic auth (JIRA_EMAIL + JIRA_API_TOKEN) when set; otherwise OAuth. Paginates Jira API to fetch beyond 100.
    """
    if not _jira_configured():
        return jsonify({
            'status': 'error',
            'message': 'Jira is not connected. Use email + API token in .env, or connect via OAuth (Tools → Jira connection).',
        }), 503

    try:
        project = request.args.get('project', 'HALO').strip() or 'HALO'
        max_results = min(max(int(request.args.get('max_results', 1000)), 1), 1000)  # default 1000, cap 1000
        ancestor_key = (request.args.get('ancestor_key') or request.args.get('parent_key') or '').strip() or None
        issuetype_arg = (request.args.get('issuetype') or 'Bug').strip()
        issuetype = None if issuetype_arg.lower() in ('', 'all', '*') else issuetype_arg
        client = JiraClient()
        issues = client.fetch_issues_for_triage(
            project=project,
            max_results=max_results,
            ancestor_key=ancestor_key,
            issuetype=issuetype,  # default from param is Bug; None means all types (e.g. ?issuetype=all)
        )
        return jsonify({
            'status': 'success',
            'data': issues,
            'count': len(issues),
        })
    except ValueError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    except requests.exceptions.HTTPError as e:
        logger.warning("Jira issues HTTP error: %s %s", e.response.status_code if e.response else None, getattr(e.response, 'text', '')[:200])
        message, error_details, status_code = _jira_http_error_response(e, 'Failed to fetch issues from Jira')
        return jsonify({
            'status': 'error',
            'message': message,
            'error_details': error_details,
        }), status_code if 400 <= status_code < 600 else 500
    except Exception as e:
        logger.exception("Jira fetch failed")
        return jsonify({
            'status': 'error',
            'message': str(e) or 'Failed to fetch issues from Jira',
        }), 500


@jira_bp.route('/backlog-overview', methods=['POST'])
def backlog_overview():
    """
    Generate an AI markdown overview from a client-supplied list of issues (same filtered set as the UI).
    Expects JSON: { "issues": [ { ... } ] }. Does not call Jira; uses Claude via service container.
    """
    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'Content-Type must be application/json'}), 400

    data = request.get_json(silent=True) or {}
    issues_in = data.get('issues')
    if not isinstance(issues_in, list):
        return jsonify({'status': 'error', 'message': 'Request body must include an "issues" array'}), 400

    sanitized: List[Dict[str, Any]] = []
    for item in issues_in:
        s = _sanitize_overview_issue(item)
        if s:
            sanitized.append(s)

    if not sanitized:
        return jsonify({
            'status': 'error',
            'message': 'No valid issues to analyze (each item needs at least a key).',
        }), 400

    total_submitted = len(sanitized)
    truncated = total_submitted > _OVERVIEW_MAX_ISSUES
    batch = sanitized[:_OVERVIEW_MAX_ISSUES]

    user_message = _format_issues_for_overview_prompt(batch, truncated, total_submitted)

    pii_config = Config.get_pii_config()
    if pii_config.get('redact_mode'):
        protector = create_pii_protector(pii_config)
        user_message = protector.redact_text(user_message)

    service_container = getattr(g, 'service_container', None)
    if not service_container:
        logger.error('Service container missing for backlog overview')
        return jsonify({
            'status': 'error',
            'message': 'Server misconfiguration: service container unavailable',
        }), 500

    claude_service = service_container.get_claude_service()
    if claude_service is None:
        return jsonify({
            'status': 'error',
            'message': 'Claude API is not configured (set ANTHROPIC_API_KEY).',
        }), 503

    try:
        claude_response = claude_service.send_message(
            message=user_message,
            model=None,
            max_tokens=2048,
            system_prompt=_BACKLOG_OVERVIEW_SYSTEM,
        )
        return jsonify({
            'status': 'success',
            'overview': claude_response.content or '',
            'meta': {
                'issue_count': len(batch),
                'truncated': truncated,
                'submitted_count': total_submitted,
                'model': claude_response.model,
            },
        })
    except Exception as e:
        logger.exception('Backlog overview Claude call failed: %s', e)
        return jsonify({
            'status': 'error',
            'message': str(e) or 'Failed to generate backlog overview',
        }), 500
