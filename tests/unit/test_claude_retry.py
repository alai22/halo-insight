"""Tests for Claude API 429 retry behavior."""

from unittest.mock import MagicMock, patch

import requests

from backend.models.response import ClaudeResponse
from backend.services import claude_service as cs_mod
from backend.services.claude_service import ClaudeService
from backend.core.exceptions import RateLimitError


def _ok_json_response():
    r = MagicMock()
    r.status_code = 200
    r.headers = {}
    r.json.return_value = {
        'content': [{'type': 'text', 'text': 'ok'}],
        'usage': {'output_tokens': 3},
    }
    return r


def _429_response(retry_after=None):
    r = MagicMock()
    r.status_code = 429
    h = {}
    if retry_after is not None:
        h['retry-after'] = str(retry_after)
    r.headers = h
    return r


@patch.object(cs_mod.Config, 'CLAUDE_RETRY_MAX_ATTEMPTS', 3)
@patch.object(cs_mod.Config, 'CLAUDE_RETRY_BASE_DELAY_SEC', 0.01)
@patch.object(cs_mod.Config, 'CLAUDE_RETRY_MAX_DELAY_SEC', 1.0)
@patch('backend.services.claude_service.time.sleep')
def test_send_message_retries_429_then_succeeds(mock_sleep):
    svc = ClaudeService(api_key='test-key')
    svc.cache_service = None

    ok = _ok_json_response()
    with patch('backend.services.claude_service.requests.post') as mock_post:
        mock_post.side_effect = [_429_response(), _429_response(1), ok]
        out = svc.send_message(message='hi', max_tokens=10, system_prompt=None)

    assert isinstance(out, ClaudeResponse)
    assert out.content == 'ok'
    assert mock_post.call_count == 3
    assert mock_sleep.call_count == 2


@patch.object(cs_mod.Config, 'CLAUDE_RETRY_MAX_ATTEMPTS', 2)
@patch.object(cs_mod.Config, 'CLAUDE_RETRY_BASE_DELAY_SEC', 0.01)
@patch.object(cs_mod.Config, 'CLAUDE_RETRY_MAX_DELAY_SEC', 1.0)
@patch('backend.services.claude_service.time.sleep')
def test_send_message_raises_after_max_429(mock_sleep):
    svc = ClaudeService(api_key='test-key')
    svc.cache_service = None

    with patch('backend.services.claude_service.requests.post') as mock_post:
        mock_post.side_effect = [_429_response(), _429_response()]
        with pytest.raises(RateLimitError) as ei:
            svc.send_message(message='hi', max_tokens=10)
    assert ei.value.details.get('attempts') == 2
    assert mock_post.call_count == 2
