"""Backlog overview partial success, structured errors, and NDJSON stream."""

import json
from unittest.mock import MagicMock, patch

import pytest

from backend.models.response import ClaudeResponse


def _issue(key='HALO-1', parent=True):
    row = {
        'key': key,
        'title': 'Test bug',
        'priority': 'Major',
        'status': 'Open',
        'description': 'Desc',
    }
    if parent:
        row['parentKey'] = 'HALO-EPIC'
    return row


def _resp(text):
    return ClaudeResponse(content=text, model='claude-test', tokens_used=10, streamed=False)


@patch('app.get_service_container')
def test_backlog_overview_partial_when_title_scan_fails(mock_get_container, client, monkeypatch):
    monkeypatch.setenv('JIRA_BACKLOG_OVERVIEW_DEEP_PASS', '0')
    monkeypatch.setenv('JIRA_BACKLOG_TITLE_REWRITE_ENABLED', '1')

    pass1 = _resp('## Duplicates\n- none\n')
    pass2 = _resp(
        '### Recommended Jira priority changes\n'
        '| Ticket | Current priority | Recommendation |\n'
        '| --- | --- | --- |\n'
        '| HALO-1 | Major | Keep |\n'
    )

    mock_claude = MagicMock()
    mock_claude.send_message.side_effect = [pass1, pass2, RuntimeError('simulated title scan failure')]

    container = MagicMock()
    container.get_claude_service.return_value = mock_claude
    mock_get_container.return_value = container

    rv = client.post(
        '/api/jira/backlog-overview',
        json={'issues': [_issue()]},
        content_type='application/json',
    )
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['status'] == 'success'
    assert '## Priority review' in (data.get('overview') or '')
    assert data['meta'].get('overview_incomplete') is True
    assert 'title_suggestions' in (data['meta'].get('omitted_sections') or [])


@patch('app.get_service_container')
def test_backlog_overview_structured_error_on_pass1(mock_get_container, client):
    mock_claude = MagicMock()
    from backend.core.exceptions import RateLimitError

    mock_claude.send_message.side_effect = RateLimitError('too many', details={'retry_after_seconds': 12})

    container = MagicMock()
    container.get_claude_service.return_value = mock_claude
    mock_get_container.return_value = container

    rv = client.post(
        '/api/jira/backlog-overview',
        json={'issues': [_issue()]},
        content_type='application/json',
    )
    assert rv.status_code == 429
    data = rv.get_json()
    assert data['status'] == 'error'
    assert data['failed_step'] == 'pass1'
    assert data['completed_steps'] == []
    assert data['retry_after_seconds'] == 12


@patch('app.get_service_container')
def test_backlog_overview_stream_emits_progress_and_result(mock_get_container, client, monkeypatch):
    monkeypatch.setenv('JIRA_BACKLOG_OVERVIEW_DEEP_PASS', '0')
    monkeypatch.setenv('JIRA_BACKLOG_TITLE_REWRITE_ENABLED', '1')
    monkeypatch.setenv('JIRA_BACKLOG_TITLE_REWRITE_DISABLED', '0')

    pass1 = _resp('## Themes\nx\n')
    pass2 = _resp(
        '### Recommended Jira priority changes\n'
        '| Ticket | Current priority | Recommendation |\n'
        '| --- | --- | --- |\n'
        '| HALO-1 | Major | Keep |\n'
    )
    title_scan = _resp('{"keys":[]}')

    mock_claude = MagicMock()
    mock_claude.send_message.side_effect = [pass1, pass2, title_scan]

    container = MagicMock()
    container.get_claude_service.return_value = mock_claude
    mock_get_container.return_value = container

    rv = client.post(
        '/api/jira/backlog-overview?stream=1',
        json={'issues': [_issue()]},
        content_type='application/json',
    )
    assert rv.status_code == 200
    assert 'ndjson' in (rv.headers.get('Content-Type') or '').lower()
    lines = [ln for ln in rv.data.decode('utf-8').split('\n') if ln.strip()]
    assert len(lines) >= 3
    events = [json.loads(ln) for ln in lines]
    assert any(e.get('type') == 'progress' and e.get('step') == 'pass1' for e in events)
    partials = [e for e in events if e.get('type') == 'partial']
    assert len(partials) >= 1
    assert partials[0].get('milestone') == 'after_pass2'
    pm0 = (partials[0].get('markdown') or '').strip()
    assert len(pm0) > 0
    terminal = [e for e in events if e.get('type') == 'result']
    assert len(terminal) == 1
    assert terminal[0]['status'] == 'success'
    assert 'overview' in terminal[0]
    final_md = (terminal[0].get('overview') or '').strip()
    assert final_md.startswith(pm0)
    meta = terminal[0].get('meta') or {}
    assert meta.get('title_rewrite_no_candidates') is True
    assert 'No tickets were selected for title rewrite' in final_md
    assert 'completed_steps' in meta and 'title_rewrite' in (meta.get('completed_steps') or [])


@patch('app.get_service_container')
def test_backlog_overview_ai_coverage_with_scorecard(mock_get_container, client):
    """Terminal meta includes ai_coverage counts for shortlist → scorecard path."""
    pass1 = _resp('## Themes\nx\n')
    shortlist = _resp('{"keys":["HALO-1"]}')
    scorecard_payload = {
        'version': '2',
        'rows': [
            {
                'key': 'HALO-1',
                'feature_importance': 2,
                'reach': 1,
                'technical_severity': 1,
                'workaround_quality': 1,
                'regression_risk': 0,
                'raw_total': 5,
                'ga_verdict': 'PostGA',
                'jira_priority': 'Normal',
            }
        ],
    }
    scorecard = _resp(json.dumps(scorecard_payload))

    mock_claude = MagicMock()
    mock_claude.send_message.side_effect = [pass1, shortlist, scorecard]

    container = MagicMock()
    container.get_claude_service.return_value = mock_claude
    mock_get_container.return_value = container

    with patch.multiple(
        'backend.api.routes.jira_routes.Config',
        JIRA_TRIAGE_SCORECARD_ENABLED=True,
        JIRA_TRIAGE_SCORECARD_INCLUDE_GA_BLOCKERS=False,
        JIRA_BACKLOG_OVERVIEW_DEEP_PASS_ENABLED=False,
        JIRA_BACKLOG_TITLE_REWRITE_ENABLED=False,
    ):
        rv = client.post(
            '/api/jira/backlog-overview',
            json={'issues': [_issue()]},
            content_type='application/json',
        )
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['status'] == 'success'
    meta = data.get('meta') or {}
    cov = meta.get('ai_coverage')
    assert isinstance(cov, dict)
    assert cov.get('issues_in_prompt_batch') == 1
    assert cov.get('issues_received_raw') == 1
    assert cov.get('shortlist_model_keys') == 1
    assert cov.get('scorecard_scored_keys') == 1
    assert cov.get('ga_blockers_in_batch') == 0
    assert cov.get('ga_blockers_included_in_scored_set') == 0
    assert cov.get('scored_keys_added_by_ga_union') == 0
    assert meta.get('scorecard_enabled') is True


@patch('app.get_service_container')
def test_backlog_overview_scorecard_parse_failure_includes_raw_debug(mock_get_container, client):
    """Invalid scorecard JSON attaches bounded pass2 excerpt in meta for debugging."""
    pass1 = _resp('## Themes\nx\n')
    shortlist = _resp('{"keys":["HALO-1"]}')
    bogus = 'not json ' + ('x' * 500)
    scorecard_bad = _resp(bogus)

    mock_claude = MagicMock()
    mock_claude.send_message.side_effect = [pass1, shortlist, scorecard_bad]

    container = MagicMock()
    container.get_claude_service.return_value = mock_claude
    mock_get_container.return_value = container

    with patch.multiple(
        'backend.api.routes.jira_routes.Config',
        JIRA_TRIAGE_SCORECARD_ENABLED=True,
        JIRA_TRIAGE_SCORECARD_INCLUDE_GA_BLOCKERS=False,
        JIRA_BACKLOG_OVERVIEW_DEEP_PASS_ENABLED=False,
        JIRA_BACKLOG_TITLE_REWRITE_ENABLED=False,
        JIRA_TRIAGE_SCORECARD_EXPOSE_RAW_ON_FAILURE=True,
        JIRA_TRIAGE_SCORECARD_FAILURE_RAW_MAX_CHARS=100,
    ):
        rv = client.post(
            '/api/jira/backlog-overview',
            json={'issues': [_issue()]},
            content_type='application/json',
        )
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['status'] == 'success'
    meta = data.get('meta') or {}
    assert meta.get('scorecard_parse_failed') is True
    dbg = meta.get('scorecard_llm_raw_debug') or {}
    assert 'pass2' in dbg
    p2 = dbg['pass2']
    assert p2['truncated'] is True
    assert p2['length'] == len(bogus)
    assert len(p2['text']) == 100
    assert p2['text'] == bogus[:100]


@patch('app.get_service_container')
def test_backlog_overview_scorecard_parse_failure_omits_raw_when_disabled(mock_get_container, client):
    """When EXPOSE_RAW_ON_FAILURE is false, meta does not include raw excerpts."""
    pass1 = _resp('## Themes\nx\n')
    shortlist = _resp('{"keys":["HALO-1"]}')
    scorecard_bad = _resp('totally invalid')

    mock_claude = MagicMock()
    mock_claude.send_message.side_effect = [pass1, shortlist, scorecard_bad]

    container = MagicMock()
    container.get_claude_service.return_value = mock_claude
    mock_get_container.return_value = container

    with patch.multiple(
        'backend.api.routes.jira_routes.Config',
        JIRA_TRIAGE_SCORECARD_ENABLED=True,
        JIRA_TRIAGE_SCORECARD_INCLUDE_GA_BLOCKERS=False,
        JIRA_BACKLOG_OVERVIEW_DEEP_PASS_ENABLED=False,
        JIRA_BACKLOG_TITLE_REWRITE_ENABLED=False,
        JIRA_TRIAGE_SCORECARD_EXPOSE_RAW_ON_FAILURE=False,
    ):
        rv = client.post(
            '/api/jira/backlog-overview',
            json={'issues': [_issue()]},
            content_type='application/json',
        )
    assert rv.status_code == 200
    meta = rv.get_json().get('meta') or {}
    assert meta.get('scorecard_parse_failed') is True
    assert meta.get('scorecard_llm_raw_debug') == {}
