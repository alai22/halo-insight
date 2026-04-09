"""
Unit tests for ConversationService
"""

import pytest
from unittest.mock import Mock, patch
from backend.services.conversation_service import ConversationService
from backend.core.interfaces import IConversationService, IStorageService
from backend.models.conversation import ConversationSummary


class TestConversationService:
    """Test suite for ConversationService"""
    
    def test_conversation_service_implements_interface(self):
        """Test that ConversationService implements IConversationService"""
        assert issubclass(ConversationService, IConversationService)
    
    def test_conversation_service_initialization(self, mock_storage_service):
        """Test ConversationService initialization"""
        service = ConversationService(storage_service=mock_storage_service)
        
        assert service.storage_service == mock_storage_service
        assert isinstance(service.conversations, list)
    
    def test_load_conversations(self, mock_storage_service):
        """Test loading conversations"""
        mock_storage_service.load_conversations.return_value = [
            {
                "conversationId": "conv_1",
                "customerId": "customer_1",
                "contentType": "CHAT_MESSAGE",
                "timestamp": "2024-01-01T00:00:00Z",
                "content": {"type": "CHAT_MESSAGE", "content": "Test", "messageType": "CUSTOMER"}
            }
        ]
        
        service = ConversationService(storage_service=mock_storage_service)
        assert len(service.conversations) == 1
        assert service.conversations[0].conversation_id == "conv_1"
    
    def test_get_summary_empty(self, mock_storage_service):
        """Test getting summary with no conversations"""
        mock_storage_service.load_conversations.return_value = []
        service = ConversationService(storage_service=mock_storage_service)
        
        summary = service.get_summary()
        assert isinstance(summary, ConversationSummary)
        assert summary.total_items == 0
        assert summary.unique_customers == 0
    
    def test_get_summary_with_data(self, mock_storage_service):
        """Test getting summary with conversation data"""
        # Note: ConversationItem.content_type looks for content.type, not contentType
        # So we need to include 'type' in the content dict
        mock_storage_service.load_conversations.return_value = [
            {
                "conversationId": "conv_1",
                "customerId": "customer_1",
                "contentType": "CHAT_MESSAGE",
                "timestamp": "2024-01-01T00:00:00Z",
                "content": {"type": "CHAT_MESSAGE", "content": "Test", "messageType": "CUSTOMER"}
            },
            {
                "conversationId": "conv_2",
                "customerId": "customer_2",
                "contentType": "EMAIL",
                "timestamp": "2024-01-02T00:00:00Z",
                "content": {"type": "EMAIL", "subject": "Test", "body": "Body"}
            }
        ]
        
        service = ConversationService(storage_service=mock_storage_service)
        summary = service.get_summary()
        
        assert summary.total_items == 2
        assert summary.unique_customers == 2
        assert summary.unique_conversations == 2
        assert 'CHAT_MESSAGE' in summary.content_types
        assert 'EMAIL' in summary.content_types
    
    def test_search_conversations(self, mock_storage_service):
        """Test searching conversations"""
        mock_storage_service.load_conversations.return_value = [
            {
                "conversationId": "conv_1",
                "customerId": "customer_1",
                "contentType": "CHAT_MESSAGE",
                "timestamp": "2024-01-01T00:00:00Z",
                "content": {"type": "CHAT_MESSAGE", "content": "Hello world", "messageType": "CUSTOMER"}
            },
            {
                "conversationId": "conv_2",
                "customerId": "customer_2",
                "contentType": "EMAIL",
                "timestamp": "2024-01-02T00:00:00Z",
                "content": {"type": "EMAIL", "subject": "Test", "body": "Goodbye"}
            }
        ]
        
        service = ConversationService(storage_service=mock_storage_service)
        results = service.search_conversations("Hello")
        
        assert len(results) == 1
        assert results[0]['conversationId'] == "conv_1"
    
    def test_search_conversations_no_results(self, mock_storage_service):
        """Test searching with no results"""
        mock_storage_service.load_conversations.return_value = [
            {
                "conversationId": "conv_1",
                "customerId": "customer_1",
                "contentType": "CHAT_MESSAGE",
                "timestamp": "2024-01-01T00:00:00Z",
                "content": {"type": "CHAT_MESSAGE", "content": "Hello", "messageType": "CUSTOMER"}
            }
        ]
        
        service = ConversationService(storage_service=mock_storage_service)
        results = service.search_conversations("Nonexistent")
        
        assert len(results) == 0
    
    def test_search_conversations_limit(self, mock_storage_service):
        """Test search respects limit parameter"""
        # Create 20 conversations
        conversations = []
        for i in range(20):
            conversations.append({
                "conversationId": f"conv_{i}",
                "customerId": f"customer_{i}",
                "contentType": "CHAT_MESSAGE",
                "timestamp": f"2024-01-{i+1:02d}T00:00:00Z",
                "content": {"type": "CHAT_MESSAGE", "content": "Hello world", "messageType": "CUSTOMER"}
            })
        
        mock_storage_service.load_conversations.return_value = conversations
        service = ConversationService(storage_service=mock_storage_service)
        
        results = service.search_conversations("Hello", limit=5)
        assert len(results) == 5

