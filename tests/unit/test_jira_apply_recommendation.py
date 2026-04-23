"""
Tests for POST /api/jira/issues/<key>/apply-recommendation
"""

from unittest.mock import MagicMock, patch

import pytest
import requests


@pytest.fixture
def jira_ready():
    with patch('backend.api.routes.jira_routes._jira_configured', return_value=True):
        yield


def test_apply_priority_updates_and_comments(jira_ready, client):
    with patch('backend.api.routes.jira_routes.JiraClient') as mock_cls:
        inst = MagicMock()
        mock_cls.return_value = inst
        inst.get_issue.return_value = {
            'fields': {
                'summary': 'Hello',
                'priority': {'name': 'Major'},
            },
        }
        inst.resolve_priority_display_name.return_value = 'Critical'

        res = client.post(
            '/api/jira/issues/HALO-1/apply-recommendation',
            json={
                'kind': 'reprior',
                'target_priority_key': 'critical',
                'expected_priority_key': 'major',
            },
        )
        assert res.status_code == 200
        data = res.get_json()
        assert data['status'] == 'success'
        assert data['updated']['priority'] is True
        inst.update_issue_fields.assert_called_once()
        inst.add_issue_comment_plain.assert_called_once()
        args = inst.add_issue_comment_plain.call_args[0]
        assert 'HALO-1' in args[0].upper() or args[0] == 'HALO-1'
        assert 'Bug Triage Copilot' in args[1]


def test_apply_stale_summary_409(jira_ready, client):
    with patch('backend.api.routes.jira_routes.JiraClient') as mock_cls:
        inst = MagicMock()
        mock_cls.return_value = inst
        inst.get_issue.return_value = {
            'fields': {
                'summary': 'Live title',
                'priority': {'name': 'Major'},
            },
        }
        res = client.post(
            '/api/jira/issues/HALO-2/apply-recommendation',
            json={
                'kind': 'title',
                'new_summary': 'New title here',
                'expected_summary': 'Different from live',
                'expected_priority_key': 'major',
            },
        )
        assert res.status_code == 409
        assert res.get_json().get('error_code') == 'STALE_LOCK'
        inst.update_issue_fields.assert_not_called()


def test_apply_no_changes_422(jira_ready, client):
    with patch('backend.api.routes.jira_routes.JiraClient') as mock_cls:
        inst = MagicMock()
        mock_cls.return_value = inst
        inst.get_issue.return_value = {
            'fields': {
                'summary': 'Same',
                'priority': {'name': 'Major'},
            },
        }
        res = client.post(
            '/api/jira/issues/HALO-3/apply-recommendation',
            json={
                'kind': 'reprior',
                'target_priority_key': 'major',
                'expected_priority_key': 'major',
            },
        )
        assert res.status_code == 422
        assert res.get_json().get('error_code') == 'NO_CHANGES'


def test_apply_jira_403_message(jira_ready, client):
    with patch('backend.api.routes.jira_routes.JiraClient') as mock_cls:
        inst = MagicMock()
        mock_cls.return_value = inst
        inst.get_issue.return_value = {
            'fields': {
                'summary': 'T',
                'priority': {'name': 'Minor'},
            },
        }
        inst.resolve_priority_display_name.return_value = 'Major'
        resp = MagicMock()
        resp.status_code = 403
        resp.text = 'Forbidden'
        err = requests.exceptions.HTTPError()
        err.response = resp
        inst.update_issue_fields.side_effect = err

        res = client.post(
            '/api/jira/issues/HALO-4/apply-recommendation',
            json={
                'kind': 'reprior',
                'target_priority_key': 'major',
                'expected_priority_key': 'minor',
            },
        )
        assert res.status_code == 403
        body = res.get_json()
        assert body.get('error_code') == 'JIRA_FORBIDDEN'
        assert 'write:jira-work' in body.get('message', '')
