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
    monkeypatch.setenv('JIRA_BACKLOG_TITLE_REWRITE_ENABLED', '0')

    pass1 = _resp('## Themes\nx\n')
    pass2 = _resp(
        '### Recommended Jira priority changes\n'
        '| Ticket | Current priority | Recommendation |\n'
        '| --- | --- | --- |\n'
        '| HALO-1 | Major | Keep |\n'
    )

    mock_claude = MagicMock()
    mock_claude.send_message.side_effect = [pass1, pass2]

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
    terminal = [e for e in events if e.get('type') == 'result']
    assert len(terminal) == 1
    assert terminal[0]['status'] == 'success'
    assert 'overview' in terminal[0]
