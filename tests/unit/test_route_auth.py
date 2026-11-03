"""Data and tool routes reject anonymous requests; the public ones stay open."""

from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def container():
    """Service container whose RAG services answer without calling Claude."""
    container = MagicMock()
    container.get_rag_service.return_value.process_query.return_value = {'answer': 'ok'}
    container.get_unified_rag_service.return_value.process_query.return_value = {'answer': 'ok'}
    with patch('app.get_service_container', return_value=container):
        yield container


# One route per blueprint: (method, path, json body)
USER_ROUTES = [
    ('get', '/api/conversations/extract-topics-status', None),
    ('post', '/api/conversations/ask', {'question': 'hi'}),
    ('post', '/api/unified/ask', {'question': 'hi'}),
    ('get', '/api/jira/status', None),
]

ADMIN_ROUTES = [
    ('get', '/api/zoom/download/status', None),
    ('get', '/api/analytics/status', None),
]


def _call(client, method, path, body):
    return getattr(client, method)(path, json=body)


@pytest.mark.parametrize('method,path,body', USER_ROUTES + ADMIN_ROUTES)
def test_anonymous_request_is_rejected(client, method, path, body):
    assert _call(client, method, path, body).status_code == 401


@pytest.mark.parametrize('method,path,body', USER_ROUTES)
def test_logged_in_user_is_allowed(auth_client, container, method, path, body):
    assert _call(auth_client, method, path, body).status_code == 200


@pytest.mark.parametrize('method,path,body', ADMIN_ROUTES)
def test_non_admin_user_is_rejected_from_admin_tools(auth_client, method, path, body):
    assert _call(auth_client, method, path, body).status_code == 401


@pytest.mark.parametrize('method,path,body', ADMIN_ROUTES)
def test_admin_is_allowed(admin_client, method, path, body):
    assert _call(admin_client, method, path, body).status_code == 200


def test_jira_oauth_requires_admin(auth_client):
    assert auth_client.get('/api/jira/oauth/authorize').status_code == 401


def test_pageview_tracking_stays_public(client):
    # The app posts pageviews from the login screen and participant pages.
    res = client.post('/api/analytics/track', json={'page_path': '/'})
    assert res.status_code != 401
