"""
Jira API Client for Bug Triage Copilot

Fetches issues from Jira Cloud via REST API v3 using Basic auth (email + API token).
Uses the JQL search endpoint (legacy /rest/api/3/search was removed and returns 410).
See: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/
"""

import base64
import re
import logging
from typing import List, Dict, Any, Optional, Tuple

import requests

from backend.utils.config import Config
from backend.utils.logging import get_logger

logger = get_logger('jira_client')


def _normalize_priority_for_match(name: str) -> str:
    """Lowercase, no spaces — aligns with jira_routes _PRIORITY_RANKS keys after alias expansion."""
    return re.sub(r'\s+', '', (name or '').strip().lower())


def _plain_text_to_adf_doc(text: str) -> Dict[str, Any]:
    """Minimal Atlassian Document Format for a comment body (paragraphs from newlines)."""
    s = (text or '').replace('\r\n', '\n').replace('\r', '\n')
    lines = s.split('\n') if s else ['']
    content: List[Dict[str, Any]] = []
    for line in lines:
        content.append({
            'type': 'paragraph',
            'content': [{'type': 'text', 'text': line}] if line else [],
        })
    return {'type': 'doc', 'version': 1, 'content': content}


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


def _parse_epic_link_field(fields: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
    """
    Epic Link value from Jira Software (company-managed) is often customfield_10014.
    Returns (epic_key_or_none, epic_summary_or_none). Summary is present only when
    Jira returns a nested issue object with fields.summary.
    """
    epic_raw = fields.get('customfield_10014')
    if epic_raw is None or epic_raw == '':
        return (None, None)
    if isinstance(epic_raw, str):
        k = epic_raw.strip()
        return (k, None) if k else (None, None)
    if isinstance(epic_raw, dict):
        k = epic_raw.get('key')
        if not k:
            return (None, None)
        epic_fields = epic_raw.get('fields') or {}
        summ = ''
        if isinstance(epic_fields, dict):
            summ = (epic_fields.get('summary') or '').strip()
        return (str(k).strip(), summ or None)
    return (None, None)


def _get_sprint_name(fields: Dict[str, Any]) -> Optional[str]:
    """Extract sprint name from issue fields. Jira Software uses customfield_10020 or similar."""
    # Common Jira Software Cloud sprint field
    sprint = fields.get('customfield_10020')
    if isinstance(sprint, dict) and sprint.get('name'):
        return sprint.get('name')
    if isinstance(sprint, list) and sprint:
        first = sprint[0]
        if isinstance(first, dict) and first.get('name'):
            return first.get('name')
    if isinstance(sprint, str):
        return sprint
    # Fallback: any field with 'sprint' in the key whose value has a name
    for k, v in fields.items():
        if 'sprint' not in k.lower():
            continue
        if isinstance(v, dict) and v.get('name'):
            return v.get('name')
        if isinstance(v, list) and v and isinstance(v[0], dict) and v[0].get('name'):
            return v[0].get('name')
    return None


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
    components = [c['name'] for c in components_list if isinstance(c, dict) and c.get('name')]
    component = components[0] if components else 'Other'
    priority_obj = fields.get('priority')
    priority_name = priority_obj.get('name') if isinstance(priority_obj, dict) and priority_obj else None
    status_obj = fields.get('status')
    status_name = status_obj.get('name') if isinstance(status_obj, dict) else None
    issuetype_obj = fields.get('issuetype')
    issuetype_name = issuetype_obj.get('name') if isinstance(issuetype_obj, dict) else None
    parent_obj = fields.get('parent')
    parent_key = None
    parent_summary = None
    if isinstance(parent_obj, dict) and parent_obj:
        parent_key = parent_obj.get('key')
        parent_fields = parent_obj.get('fields') or {}
        if isinstance(parent_fields, dict):
            parent_summary = (parent_fields.get('summary') or '').strip() or None
    epic_key, epic_summary = _parse_epic_link_field(fields)
    assignee_obj = fields.get('assignee')
    assignee_name = assignee_obj.get('displayName') if isinstance(assignee_obj, dict) and assignee_obj else None
    sprint_name = _get_sprint_name(fields)

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
        'components': components,
        'labels': labels,
        'needsMoreInfo': needs_more_info,
        'gaBlocker': ga_blocker,
        'rank': rank,
        'status': status_name,
        'issuetype': issuetype_name,
        'priority': priority_name,
        'parentKey': parent_key,
        'parentSummary': parent_summary,
        'epicKey': epic_key,
        'epicSummary': epic_summary,
        'assignee': assignee_name,
        'sprint': sprint_name,
        'aiRecommendation': {},
    }


def _has_parent_context(issue: Dict[str, Any]) -> bool:
    """Keep issue when it belongs to a parent/epic context."""
    parent_key = str(issue.get('parentKey') or '').strip()
    epic_key = str(issue.get('epicKey') or '').strip()
    return bool(parent_key or epic_key)


class JiraClient:
    """Client for Jira Cloud REST API v3. Prefers Basic auth (email + API token) when set; otherwise uses OAuth."""

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
            basic_configured = bool(self.base_url and self.email and self.api_token)
            if basic_configured:
                self._use_oauth = False
            else:
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

    def get_myself(self) -> Dict[str, Any]:
        """Current user (validates auth). GET /rest/api/3/myself."""
        response = self._request('GET', '/rest/api/3/myself')
        response.raise_for_status()
        return response.json()

    def get_projects(self) -> List[Dict[str, Any]]:
        """Projects visible to the current user. GET /rest/api/3/project."""
        response = self._request('GET', '/rest/api/3/project')
        response.raise_for_status()
        data = response.json()
        return data if isinstance(data, list) else (data.get('values') or [])

    def search_issues(
        self,
        project: str = 'HALO',
        jql: Optional[str] = None,
        max_results: int = 100,
        next_page_token: Optional[str] = None,
        fields: Optional[List[str]] = None,
        issuetype: Optional[str] = None,
        require_parent_context: bool = False,
    ) -> Dict[str, Any]:
        """
        Search issues using JQL via POST /rest/api/3/search/jql (GET can return 0 issues;
        legacy /search was removed and returns 410). Returns raw API response with
        'issues' list and optional 'nextPageToken'. If jql is not provided, builds
        project + optional issuetype (e.g. "Bug") and ORDER BY updated DESC.
        """
        if jql is None:
            # POST accepts project-scoped JQL; GET often returns 0 or "unbounded" for same query
            base = f"project = {project}"
            if issuetype:
                base += f' AND issuetype = "{issuetype}"'
            if require_parent_context:
                # Best-effort server-side narrowing; deterministic filter still runs after mapping.
                base += ' AND (parent IS NOT EMPTY OR "Epic Link" IS NOT EMPTY)'
            jql = f"{base} ORDER BY updated DESC"
        field_list = fields or [
            'summary', 'description', 'issuetype', 'components', 'priority',
            'labels', 'status', 'created', 'updated', 'parent', 'assignee',
            'customfield_10020',  # Sprint (Jira Software Cloud common id)
            'customfield_10014',  # Epic Link (common Jira Software Cloud id)
        ]
        payload = {
            'jql': jql,
            'maxResults': min(max_results, 100),
            'fields': field_list if isinstance(field_list, list) else field_list.split(','),
        }
        if next_page_token:
            payload['nextPageToken'] = next_page_token

        response = self._request('POST', '/rest/api/3/search/jql', json=payload)
        response.raise_for_status()
        return response.json()

    def fetch_issues_for_triage(
        self,
        project: str = 'HALO',
        max_results: int = 100,
        ancestor_key: Optional[str] = None,
        issuetype: Optional[str] = 'Bug',
        require_parent_context: bool = True,
    ) -> Dict[str, Any]:
        """
        Fetch issues for the given project and return them in Bug Triage Copilot shape.
        Jira's API returns at most 100 per request; we paginate with nextPageToken to fetch up to max_results.
        If ancestor_key is set (e.g. HALO-23306), only return issues that are that issue or its descendants.
        issuetype filters by Jira issue type (default "Bug"); pass None or empty to fetch all types.
        """
        all_issues: List[Dict] = []
        next_page_token: Optional[str] = None
        page_size = 100  # Jira search/jql max per request

        while len(all_issues) < max_results:
            to_fetch = min(page_size, max_results - len(all_issues))
            data = self.search_issues(
                project=project,
                max_results=to_fetch,
                next_page_token=next_page_token,
                issuetype=issuetype,
                require_parent_context=require_parent_context,
            )
            page = data.get('issues') or []
            all_issues.extend(page)
            next_page_token = data.get('nextPageToken')
            if not next_page_token or len(page) < to_fetch:
                break

        mapped = [_map_jira_issue_to_triage(issue) for issue in all_issues[:max_results]]
        before_parent_filter = len(mapped)
        if require_parent_context:
            mapped = [i for i in mapped if _has_parent_context(i)]
        if ancestor_key:
            mapped = _filter_issues_under_ancestor(mapped, ancestor_key)
        return {
            'issues': mapped,
            'count_before_parent_filter': before_parent_filter,
            'count_after_parent_filter': len(mapped),
            'parent_filter_applied': bool(require_parent_context),
        }

    def get_issue(self, issue_key: str, fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """GET /rest/api/3/issue/{issueIdOrKey} with explicit fields list."""
        key = (issue_key or '').strip()
        if not key:
            raise ValueError('issue_key is required')
        field_list = fields or ['summary', 'priority']
        params = ','.join(field_list)
        response = self._request('GET', f'/rest/api/3/issue/{key}', params={'fields': params})
        response.raise_for_status()
        return response.json()

    def update_issue_fields(self, issue_key: str, fields_update: Dict[str, Any]) -> None:
        """PUT /rest/api/3/issue/{issueIdOrKey} — fields_update is Jira API shape (summary, priority, …)."""
        key = (issue_key or '').strip()
        if not key:
            raise ValueError('issue_key is required')
        if not fields_update:
            raise ValueError('fields_update is empty')
        payload = {'fields': fields_update}
        response = self._request('PUT', f'/rest/api/3/issue/{key}', json=payload)
        response.raise_for_status()

    def add_issue_comment_plain(self, issue_key: str, text: str) -> Dict[str, Any]:
        """POST /rest/api/3/issue/{issueIdOrKey}/comment with ADF body built from plain text."""
        key = (issue_key or '').strip()
        if not key:
            raise ValueError('issue_key is required')
        body = _plain_text_to_adf_doc(text)
        response = self._request(
            'POST',
            f'/rest/api/3/issue/{key}/comment',
            json={'body': body},
        )
        response.raise_for_status()
        data = response.json()
        return data if isinstance(data, dict) else {}

    def list_priorities(self) -> List[Dict[str, Any]]:
        """GET /rest/api/3/priority — global priority list for the Jira instance."""
        response = self._request('GET', '/rest/api/3/priority')
        response.raise_for_status()
        data = response.json()
        return data if isinstance(data, list) else []

    def resolve_priority_display_name(self, normalized_key: str) -> str:
        """
        Map a normalized ladder key (e.g. critical, major) to this site's exact Jira priority.name.
        Falls back to title-cased key if the API list does not match.
        """
        nk = _normalize_priority_for_match(normalized_key)
        if not nk:
            raise ValueError('normalized_key is empty')

        alias_to_canonical = {
            'highest': 'blocker',
            'high': 'major',
            'medium': 'normal',
            'low': 'minor',
            'lowest': 'trivial',
        }
        canonical = alias_to_canonical.get(nk, nk)

        fallback_title = {
            'blocker': 'Blocker',
            'critical': 'Critical',
            'major': 'Major',
            'normal': 'Normal',
            'minor': 'Minor',
            'trivial': 'Trivial',
        }.get(canonical, canonical[:1].upper() + canonical[1:] if canonical else '')

        try:
            plist = self.list_priorities()
        except Exception as e:
            logger.warning('list_priorities failed; using fallback name for %s: %s', nk, e)
            return fallback_title

        for p in plist:
            if not isinstance(p, dict):
                continue
            name = (p.get('name') or '').strip()
            if not name:
                continue
            nm = _normalize_priority_for_match(name)
            if nm == canonical or nm == nk:
                return name
            if alias_to_canonical.get(nm) == canonical:
                return name

        return fallback_title


def _filter_issues_under_ancestor(issues: List[Dict[str, Any]], ancestor_key: str) -> List[Dict[str, Any]]:
    """
    Keep only issues that are the ancestor_key itself or a descendant (child, grandchild, etc.).
    ancestor_key is the root issue key (e.g. HALO-23306). Uses parentKey on each issue.
    """
    if not ancestor_key or not issues:
        return issues
    ancestor_key = ancestor_key.strip().upper()
    # Case-insensitive lookup by normalized key
    key_to_issue = {((i.get('key') or '').upper()): i for i in issues}

    def is_under_ancestor(issue: Dict[str, Any]) -> bool:
        current = issue
        seen = set()
        while current:
            k = (current.get('key') or '').upper()
            if k == ancestor_key:
                return True
            if k in seen:
                break
            seen.add(k)
            parent_k = (current.get('parentKey') or '').strip().upper()
            if not parent_k:
                return False
            current = key_to_issue.get(parent_k)
            if not current:
                # Parent not in fetched set; can't confirm
                return False
        return False

    return [i for i in issues if is_under_ancestor(i)]
