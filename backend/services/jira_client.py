"""
Jira API Client for Bug Triage Copilot

Fetches issues from Jira Cloud via REST API v3 using Basic auth (email + API token).
Uses the JQL search endpoint (legacy /rest/api/3/search was removed and returns 410).
See: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/
"""

import base64
import re
import logging
from typing import List, Dict, Any, Optional

import requests

from backend.utils.config import Config
from backend.utils.logging import get_logger

logger = get_logger('jira_client')


def _adf_to_plain_text(adf: Any) -> str:
    """Extract plain text from Jira's Atlassian Document Format (ADF) description."""
    if not adf:
        return ''
    if isinstance(adf, str):
        return adf.strip()
    text_parts = []

    def walk(node):
        if isinstance(node, dict):
            if node.get('type') == 'text' and 'text' in node:
                text_parts.append(node['text'])
            for key in ('content', 'text'):
                if key in node and isinstance(node[key], list):
                    for child in node[key]:
                        walk(child)
                elif key in node and isinstance(node[key], str):
                    text_parts.append(node[key])
        elif isinstance(node, list):
            for child in node:
                walk(child)

    walk(adf)
    return ' '.join(text_parts).strip() if text_parts else ''


def _map_jira_issue_to_triage(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Map a Jira API issue to Bug Triage Copilot issue shape."""
    key = raw.get('key', '')
    issue_id = str(raw.get('id', key))
    fields = raw.get('fields') or {}
    summary = (fields.get('summary') or '').strip()
    description_obj = fields.get('description')
    description = _adf_to_plain_text(description_obj) if description_obj else ''
    created = fields.get('created') or ''
    updated = fields.get('updated') or created
    labels = fields.get('labels') or []
    components_list = fields.get('components') or []
    component = components_list[0]['name'] if components_list else 'Other'
    priority_obj = fields.get('priority')
    priority_name = priority_obj.get('name') if isinstance(priority_obj, dict) and priority_obj else None
    status_obj = fields.get('status')
    status_name = status_obj.get('name') if isinstance(status_obj, dict) else None
    issuetype_obj = fields.get('issuetype')
    issuetype_name = issuetype_obj.get('name') if isinstance(issuetype_obj, dict) else None

    # Infer platform from labels (e.g. iOS, Android, Backend) or default
    platform_labels = {'iOS', 'Android', 'Backend', 'Other'}
    platform = 'Other'
    for lab in labels:
        if lab in platform_labels:
            platform = lab
            break

    # GA blocker / needs more info from labels (common conventions)
    label_lower = [lb.lower() for lb in labels]
    ga_blocker = 'ga-blocker' in label_lower or 'ga_blocker' in label_lower
    needs_more_info = 'needs-more-info' in label_lower or 'needs_more_info' in label_lower

    # Optional rank: use priority order (Highest=1 -> Lowest=5) or leave null
    rank = None
    if priority_name:
        rank_map = {'Highest': 95, 'High': 75, 'Medium': 50, 'Low': 25, 'Lowest': 10}
        rank = rank_map.get(priority_name)

    return {
        'id': issue_id,
        'key': key,
        'title': summary,
        'created': created,
        'updated': updated,
        'description': description[:2000] if description else None,
        'platform': platform,
        'component': component,
        'labels': labels,
        'needsMoreInfo': needs_more_info,
        'gaBlocker': ga_blocker,
        'rank': rank,
        'status': status_name,
        'issuetype': issuetype_name,
        'priority': priority_name,
        'aiRecommendation': {},
    }


class JiraClient:
    """Client for Jira Cloud REST API v3. Uses OAuth if tokens exist, else Basic auth (email + API token)."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        email: Optional[str] = None,
        api_token: Optional[str] = None,
        use_oauth: Optional[bool] = None,
    ):
        self.base_url = (base_url or Config.JIRA_BASE_URL or '').rstrip('/')
        self.email = (email or Config.JIRA_EMAIL or '').strip()
        self.api_token = (api_token or Config.JIRA_API_TOKEN or '').strip()

        if use_oauth is None:
            from backend.services import jira_oauth
            self._use_oauth = bool(
                self.base_url
                and Config.JIRA_CLIENT_ID
                and Config.JIRA_CLIENT_SECRET
                and jira_oauth.get_valid_access_token()
            )
        else:
            self._use_oauth = use_oauth

        if self._use_oauth:
            if not self.base_url:
                raise ValueError("JIRA_BASE_URL is required")
            logger.info("JiraClient initialized for %s (OAuth)", self.base_url)
        else:
            if not self.base_url or not self.email or not self.api_token:
                missing = []
                if not self.base_url:
                    missing.append('JIRA_BASE_URL')
                if not self.email:
                    missing.append('JIRA_EMAIL')
                if not self.api_token:
                    missing.append('JIRA_API_TOKEN')
                raise ValueError(
                    f"Missing Jira credentials: {', '.join(missing)}. "
                    "Set them in .env, or connect via OAuth (Tools → Jira connection)."
                )
            self._auth_header = self._make_basic_auth_header()
            logger.info("JiraClient initialized for %s (Basic auth)", self.base_url)

    def _make_basic_auth_header(self) -> str:
        credentials = f"{self.email}:{self.api_token}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded}"

    def _get_authorization_header(self) -> str:
        if self._use_oauth:
            from backend.services import jira_oauth
            token = jira_oauth.get_valid_access_token()
            if not token:
                raise ValueError("Jira OAuth token expired or missing; please reconnect (Tools → Jira connection).")
            return f"Bearer {token}"
        return self._auth_header

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': self._get_authorization_header(),
        }
        kwargs.setdefault('timeout', 30)
        return requests.request(method, url, headers=headers, **kwargs)

    def search_issues(
        self,
        project: str = 'HALO',
        jql: Optional[str] = None,
        max_results: int = 100,
        next_page_token: Optional[str] = None,
        fields: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Search issues using JQL via /rest/api/3/search/jql (legacy /search returns 410).
        Returns raw API response with 'issues' list and optional 'nextPageToken'.
        """
        if jql is None:
            jql = f"project = {project} ORDER BY updated DESC"
        params = {
            'jql': jql,
            'maxResults': min(max_results, 100),
        }
        if next_page_token:
            params['nextPageToken'] = next_page_token
        if fields:
            params['fields'] = ','.join(fields)
        else:
            params['fields'] = 'summary,description,issuetype,components,priority,labels,status,created,updated'

        response = self._request('GET', '/rest/api/3/search/jql', params=params)
        response.raise_for_status()
        return response.json()

    def fetch_issues_for_triage(
        self,
        project: str = 'HALO',
        max_results: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Fetch issues for the given project and return them in Bug Triage Copilot shape.
        """
        data = self.search_issues(project=project, max_results=max_results)
        issues = data.get('issues') or []
        return [_map_jira_issue_to_triage(issue) for issue in issues]
