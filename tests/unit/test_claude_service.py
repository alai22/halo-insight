"""
Unit tests for ClaudeService
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from backend.services.claude_service import ClaudeService
from backend.models.response import ClaudeResponse
from backend.core.interfaces import IClaudeService
from backend.core.exceptions import ConfigurationError, TimeoutError as AppTimeoutError


class TestClaudeService:
    """Test suite for ClaudeService"""
    
    def test_claude_service_implements_interface(self):
        """Test that ClaudeService implements IClaudeService"""
        assert issubclass(ClaudeService, IClaudeService)
    
    @patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-api-key'})
    def test_claude_service_initialization_with_api_key(self):
        """Test ClaudeService initialization with API key"""
        service = ClaudeService(api_key='test-api-key')
        assert service.api_key == 'test-api-key'
        assert service.base_url == "https://api.anthropic.com/v1"
        assert 'x-api-key' in service.headers
    
    def test_claude_service_initialization_without_api_key(self):
        """Test ClaudeService initialization fails without API key"""
        # Mock Config.ANTHROPIC_API_KEY to be None
        with patch('backend.services.claude_service.Config.ANTHROPIC_API_KEY', None):
            with pytest.raises(ConfigurationError, match="API key not provided"):
                ClaudeService(api_key=None)
    
    @patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-api-key'})
    @patch('backend.services.claude_service.requests.post')
    def test_send_message_success(self, mock_post):
        """Test successful message sending"""
        # Mock API response
        mock_response = Mock()
        mock_response.json.return_value = {
            'content': [{'type': 'text', 'text': 'Hello, Claude!'}],
            'usage': {'output_tokens': 10, 'input_tokens': 5}
        }
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        service = ClaudeService(api_key='test-api-key')
        response = service.send_message("Hello")
        
        assert isinstance(response, ClaudeResponse)
        assert response.content == "Hello, Claude!"
        assert response.tokens_used == 10
        mock_post.assert_called_once()
        sent = mock_post.call_args[1]['json']
        assert 'temperature' not in sent
    
    @patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-api-key'})
    @patch('backend.services.claude_service.requests.post')
    def test_send_message_includes_temperature_when_set(self, mock_post):
        """Explicit temperature is forwarded in the API payload."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'content': [{'type': 'text', 'text': 'ok'}],
            'usage': {'output_tokens': 1}
        }
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        service = ClaudeService(api_key='test-api-key')
        service.send_message('Hello', max_tokens=10, temperature=0.0)

        sent = mock_post.call_args[1]['json']
        assert sent.get('temperature') == 0.0

    @patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-api-key'})
    @patch('backend.services.claude_service.requests.post')
    def test_send_message_with_system_prompt(self, mock_post):
        """Test sending message with system prompt"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'content': [{'type': 'text', 'text': 'Response'}],
            'usage': {'output_tokens': 5}
        }
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        service = ClaudeService(api_key='test-api-key')
        service.send_message("Hello", system_prompt="You are a helpful assistant")
        
        call_args = mock_post.call_args
        assert 'system' in call_args[1]['json']
        assert call_args[1]['json']['system'] == "You are a helpful assistant"
    
    @patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-api-key'})
    @patch('backend.services.claude_service.requests.post')
    def test_send_message_timeout(self, mock_post):
        """Test handling of timeout errors"""
        import requests
        mock_post.side_effect = requests.exceptions.Timeout("Request timed out")
        
        service = ClaudeService(api_key='test-api-key')
        with pytest.raises(AppTimeoutError):
            service.send_message("Hello")
    
    @patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-api-key'})
    @patch('backend.services.claude_service.requests.post')
    def test_stream_message_success(self, mock_post):
        """Test successful message streaming"""
        # Mock streaming response
        mock_response = Mock()
        mock_response.iter_lines.return_value = [
            b'data: {"type": "content_block_delta", "delta": {"text": "Hello"}}',
            b'data: {"type": "content_block_delta", "delta": {"text": " World"}}',
            b'data: [DONE]'
        ]
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        service = ClaudeService(api_key='test-api-key')
        chunks = list(service.stream_message("Hello"))
        
        assert len(chunks) == 2
        assert chunks[0]['type'] == 'content_block_delta'
    
    @patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-api-key'})
    @patch('backend.services.claude_service.requests.post')
    def test_is_available_success(self, mock_post):
        """Test service availability check"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        service = ClaudeService(api_key='test-api-key')
        assert service.is_available() is True
    
    @patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-api-key'})
    @patch('backend.services.claude_service.requests.post')
    def test_is_available_failure(self, mock_post):
        """Test service availability check when unavailable"""
        import requests
        mock_post.side_effect = requests.exceptions.RequestException("Connection error")
        
        service = ClaudeService(api_key='test-api-key')
        assert service.is_available() is False

