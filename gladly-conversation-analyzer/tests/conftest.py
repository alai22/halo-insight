"""
Pytest configuration and shared fixtures
"""

import pytest
import os
from unittest.mock import Mock, MagicMock
from typing import Generator

# Set test environment variables before importing app
os.environ['FLASK_ENV'] = 'testing'
os.environ['STORAGE_TYPE'] = 'local'
os.environ['LOCAL_FILE_PATH'] = 'tests/fixtures/test_conversations.jsonl'

from flask import Flask
from backend.core.service_container import ServiceContainer
from backend.core.interfaces import IStorageService, IClaudeService, IConversationService
from backend.models.response import ClaudeResponse


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    """Create Flask application for testing"""
    from app import create_app
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        yield app


@pytest.fixture
def client(app: Flask):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def mock_storage_service() -> IStorageService:
    """Create a mock storage service"""
    mock = Mock(spec=IStorageService)
    # Note: ConversationItem.content_type looks for content.type, so include it
    mock.load_conversations.return_value = [
        {
            "conversationId": "test_conv_1",
            "customerId": "test_customer_1",
            "contentType": "CHAT_MESSAGE",
            "timestamp": "2024-01-01T00:00:00Z",
            "content": {
                "type": "CHAT_MESSAGE",  # Include type for content_type property
                "content": "Test message",
                "messageType": "CUSTOMER"
            }
        },
        {
            "conversationId": "test_conv_2",
            "customerId": "test_customer_2",
            "contentType": "EMAIL",
            "timestamp": "2024-01-02T00:00:00Z",
            "content": {
                "type": "EMAIL",  # Include type for content_type property
                "subject": "Test email",
                "body": "Test email body"
            }
        }
    ]
    return mock


@pytest.fixture
def mock_claude_service() -> IClaudeService:
    """Create a mock Claude service"""
    mock = Mock(spec=IClaudeService)
    
    # Mock send_message
    mock_response = ClaudeResponse(
        content="Test response from Claude",
        model="claude-3-haiku-20240307",
        tokens_used=100,
        streamed=False
    )
    mock.send_message.return_value = mock_response
    
    # Mock stream_message
    def mock_stream():
        yield {"type": "content_block_delta", "delta": {"text": "Test"}}
        yield {"type": "content_block_delta", "delta": {"text": " response"}}
        yield {"type": "message_stop", "stop_reason": "end_turn"}
    
    mock.stream_message.return_value = mock_stream()
    mock.is_available.return_value = True
    
    return mock


@pytest.fixture
def service_container(mock_storage_service, mock_claude_service) -> ServiceContainer:
    """Create a service container with mocked services"""
    container = ServiceContainer()
    container.get_storage_service(override=mock_storage_service)
    container.get_claude_service(override=mock_claude_service)
    return container


@pytest.fixture
def sample_conversations():
    """Sample conversation data for testing"""
    return [
        {
            "conversationId": "conv_1",
            "customerId": "customer_1",
            "contentType": "CHAT_MESSAGE",
            "timestamp": "2024-01-01T10:00:00Z",
            "content": {
                "content": "Hello, I need help with my order",
                "messageType": "CUSTOMER"
            }
        },
        {
            "conversationId": "conv_1",
            "customerId": "customer_1",
            "contentType": "CHAT_MESSAGE",
            "timestamp": "2024-01-01T10:01:00Z",
            "content": {
                "content": "I can help you with that. What's your order number?",
                "messageType": "AGENT"
            }
        },
        {
            "conversationId": "conv_2",
            "customerId": "customer_2",
            "contentType": "EMAIL",
            "timestamp": "2024-01-02T14:30:00Z",
            "content": {
                "subject": "Refund request",
                "body": "I would like to request a refund for my recent purchase."
            }
        }
    ]


@pytest.fixture(autouse=True)
def reset_environment(monkeypatch):
    """Reset environment variables for each test"""
    # Store original values
    original_env = {}
    test_vars = {
        'ANTHROPIC_API_KEY': 'test-api-key',
        'STORAGE_TYPE': 'local',
        'LOCAL_FILE_PATH': 'tests/fixtures/test_conversations.jsonl',
        'FLASK_ENV': 'testing'
    }
    
    for key, value in test_vars.items():
        original_env[key] = os.environ.get(key)
        monkeypatch.setenv(key, value)
    
    yield
    
    # Restore original values
    for key, original_value in original_env.items():
        if original_value is None:
            monkeypatch.delenv(key, raising=False)
        else:
            monkeypatch.setenv(key, original_value)

