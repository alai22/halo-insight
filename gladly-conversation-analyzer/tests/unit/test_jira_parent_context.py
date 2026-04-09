"""
Tests for parent/epic context filtering behavior.
"""

from unittest.mock import patch

from backend.api.routes.jira_routes import _issue_has_parent_context
from backend.services.jira_client import _has_parent_context


def test_parent_context_predicate_keeps_parent_or_epic():
    assert _issue_has_parent_context({'parentKey': 'HALO-1', 'epicKey': None}) is True
    assert _issue_has_parent_context({'parentKey': '', 'epicKey': 'HALO-EPIC'}) is True
    assert _issue_has_parent_context({'parentKey': None, 'epicKey': None}) is False

    assert _has_parent_context({'parentKey': 'HALO-2', 'epicKey': ''}) is True
    assert _has_parent_context({'parentKey': '', 'epicKey': 'HALO-3'}) is True
    assert _has_parent_context({'parentKey': '', 'epicKey': ''}) is False


def test_issues_route_returns_parent_filter_metadata(client):
    with patch('backend.api.routes.jira_routes._jira_configured', return_value=True), patch(
        'backend.api.routes.jira_routes.JiraClient'
    ) as mock_client_cls:
        mock_client = mock_client_cls.return_value
        mock_client.fetch_issues_for_triage.return_value = {
            'issues': [{'key': 'HALO-10'}],
            'count_before_parent_filter': 5,
            'count_after_parent_filter': 1,
            'parent_filter_applied': True,
        }

        res = client.get('/api/jira/issues?project=HALO&require_parent_context=1')
        assert res.status_code == 200
        body = res.get_json()
        assert body['status'] == 'success'
        assert body['count'] == 1
        assert body['count_before_parent_filter'] == 5
        assert body['count_after_parent_filter'] == 1
        assert body['parent_filter_applied'] is True
        assert body['max_results_requested'] == 1000

        kwargs = mock_client.fetch_issues_for_triage.call_args.kwargs
        assert kwargs['require_parent_context'] is True


def test_issues_route_echoes_max_results_requested(client):
    with patch('backend.api.routes.jira_routes._jira_configured', return_value=True), patch(
        'backend.api.routes.jira_routes.JiraClient'
    ) as mock_client_cls:
        mock_client = mock_client_cls.return_value
        mock_client.fetch_issues_for_triage.return_value = {
            'issues': [],
            'count_before_parent_filter': 0,
            'count_after_parent_filter': 0,
            'parent_filter_applied': False,
        }
        res = client.get('/api/jira/issues?project=HALO&max_results=250')
        assert res.status_code == 200
        body = res.get_json()
        assert body['max_results_requested'] == 250
        assert mock_client.fetch_issues_for_triage.call_args.kwargs['max_results'] == 250


def test_issues_route_accepts_include_unparented_flag(client):
    with patch('backend.api.routes.jira_routes._jira_configured', return_value=True), patch(
        'backend.api.routes.jira_routes.JiraClient'
    ) as mock_client_cls:
        mock_client = mock_client_cls.return_value
        mock_client.fetch_issues_for_triage.return_value = {
            'issues': [{'key': 'HALO-10'}, {'key': 'HALO-11'}],
            'count_before_parent_filter': 2,
            'count_after_parent_filter': 2,
            'parent_filter_applied': False,
        }

        res = client.get('/api/jira/issues?project=HALO&require_parent_context=0')
        assert res.status_code == 200
        body = res.get_json()
        assert body['status'] == 'success'
        assert body['count'] == 2
        assert body['parent_filter_applied'] is False
        assert body['max_results_requested'] == 1000

        kwargs = mock_client.fetch_issues_for_triage.call_args.kwargs
        assert kwargs['require_parent_context'] is False
