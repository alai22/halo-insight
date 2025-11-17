"""
Integration tests for API routes
"""

import pytest
import json
from flask import g
from unittest.mock import patch


class TestHealthRoutes:
    """Test suite for health check endpoints"""
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'status' in data
        assert data['status'] == 'ok'


class TestClaudeRoutes:
    """Test suite for Claude API routes"""
    
    def test_claude_chat_missing_message(self, client):
        """Test Claude chat endpoint with missing message"""
        response = client.post('/api/claude/chat', json={})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_claude_chat_with_mock_service(self, client, mock_claude_service):
        """Test Claude chat endpoint with mocked service"""
        # Patch the service container to return our mock
        with patch('app.get_service_container') as mock_get_container:
            from backend.core.service_container import ServiceContainer
            container = ServiceContainer()
            container.get_claude_service(override=mock_claude_service)
            mock_get_container.return_value = container
            
            response = client.post('/api/claude/chat', json={
                'message': 'Hello',
                'model': 'claude-3-haiku-20240307'
            })
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['success'] is True
            assert 'response' in data
    
    def test_claude_chat_streaming(self, client, mock_claude_service):
        """Test Claude chat endpoint with streaming"""
        with patch('app.get_service_container') as mock_get_container:
            from backend.core.service_container import ServiceContainer
            container = ServiceContainer()
            container.get_claude_service(override=mock_claude_service)
            mock_get_container.return_value = container
            
            response = client.post('/api/claude/chat', json={
                'message': 'Hello',
                'stream': True
            })
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['success'] is True
            assert data['streamed'] is True


class TestConversationRoutes:
    """Test suite for conversation API routes"""
    
    def test_conversation_summary(self, client, mock_storage_service):
        """Test conversation summary endpoint"""
        with patch('app.get_service_container') as mock_get_container:
            from backend.core.service_container import ServiceContainer
            container = ServiceContainer()
            container.get_storage_service(override=mock_storage_service)
            mock_get_container.return_value = container
            
            response = client.get('/api/conversations/summary')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'total_items' in data
            assert 'unique_customers' in data
    
    def test_conversation_search(self, client, mock_storage_service):
        """Test conversation search endpoint"""
        with patch('app.get_service_container') as mock_get_container:
            from backend.core.service_container import ServiceContainer
            container = ServiceContainer()
            container.get_storage_service(override=mock_storage_service)
            mock_get_container.return_value = container
            
            response = client.post('/api/conversations/search', json={
                'query': 'test',
                'limit': 10
            })
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'results' in data or 'items' in data
    
    def test_conversation_search_missing_query(self, client):
        """Test conversation search with missing query"""
        response = client.post('/api/conversations/search', json={})
        assert response.status_code == 400


class TestServiceContainerIntegration:
    """Test service container integration with routes"""
    
    def test_service_container_in_request_context(self, app, mock_storage_service, mock_claude_service):
        """Test that service container is available in request context"""
        with app.app_context():
            from backend.core.service_container import ServiceContainer
            container = ServiceContainer()
            container.get_storage_service(override=mock_storage_service)
            container.get_claude_service(override=mock_claude_service)
            g.service_container = container
            
            assert g.service_container is not None
            assert g.service_container.get_storage_service() == mock_storage_service
            assert g.service_container.get_claude_service() == mock_claude_service

