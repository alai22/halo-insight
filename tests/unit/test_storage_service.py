"""
Unit tests for StorageService
"""

import pytest
import json
import os
from unittest.mock import Mock, patch, mock_open
from backend.services.storage_service import StorageService
from backend.core.interfaces import IStorageService


class TestStorageService:
    """Test suite for StorageService"""
    
    def test_storage_service_implements_interface(self):
        """Test that StorageService implements IStorageService"""
        assert issubclass(StorageService, IStorageService)
    
    @patch.dict('os.environ', {'STORAGE_TYPE': 'local', 'LOCAL_FILE_PATH': 'test.jsonl'})
    def test_storage_service_initialization_local(self):
        """Test StorageService initialization with local storage"""
        service = StorageService(storage_type='local')
        assert service.storage_type == 'local'
        assert hasattr(service, 'local_file')
    
    @patch.dict('os.environ', {'STORAGE_TYPE': 'local', 'LOCAL_FILE_PATH': 'tests/fixtures/test_conversations.jsonl'})
    def test_load_conversations_from_local(self):
        """Test loading conversations from local file"""
        service = StorageService(storage_type='local')
        conversations = service.load_conversations()
        
        assert isinstance(conversations, list)
        assert len(conversations) > 0
    
    @patch.dict('os.environ', {'STORAGE_TYPE': 'local', 'LOCAL_FILE_PATH': 'nonexistent.jsonl'})
    def test_load_conversations_nonexistent_file(self):
        """Test loading conversations from nonexistent file"""
        service = StorageService(storage_type='local')
        conversations = service.load_conversations()
        
        # Should return empty list on error
        assert isinstance(conversations, list)
    
    def test_parse_content_jsonl(self):
        """Test parsing JSONL content"""
        service = StorageService(storage_type='local')
        content = '{"id": 1}\n{"id": 2}\n'
        result = service._parse_content(content)
        
        assert len(result) == 2
        assert result[0]['id'] == 1
        assert result[1]['id'] == 2
    
    def test_parse_content_json_array(self):
        """Test parsing JSON array content"""
        service = StorageService(storage_type='local')
        content = '[{"id": 1}, {"id": 2}]'
        result = service._parse_content(content)
        
        assert len(result) == 2
        assert result[0]['id'] == 1
    
    def test_parse_content_invalid_json(self):
        """Test parsing invalid JSON content"""
        service = StorageService(storage_type='local')
        content = 'invalid json content'
        result = service._parse_content(content)
        
        # Should return empty list on parse error
        assert isinstance(result, list)
    
    @patch('backend.services.storage_service.requests.get')
    @patch.dict('os.environ', {
        'STORAGE_TYPE': 's3',
        'S3_BUCKET_NAME': 'test-bucket',
        'S3_FILE_KEY': 'test.jsonl',
        'S3_REGION': 'us-east-1'
    })
    def test_load_from_s3_public(self, mock_get):
        """Test loading from public S3 URL"""
        mock_response = Mock()
        mock_response.text = '{"id": 1}\n{"id": 2}\n'
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        service = StorageService(storage_type='s3')
        conversations = service._load_from_s3()
        
        assert len(conversations) == 2
        mock_get.assert_called_once()
    
    @patch('backend.services.storage_service.boto3.client')
    @patch.dict('os.environ', {
        'STORAGE_TYPE': 's3',
        'S3_BUCKET_NAME': 'test-bucket',
        'S3_FILE_KEY': 'test.jsonl',
        'S3_REGION': 'us-east-1'
    })
    def test_load_from_s3_authenticated(self, mock_boto3):
        """Test loading from authenticated S3"""
        mock_s3_client = Mock()
        mock_response = Mock()
        mock_response.read.return_value.decode.return_value = '{"id": 1}\n'
        mock_s3_client.get_object.return_value = {'Body': mock_response}
        mock_boto3.return_value = mock_s3_client
        
        service = StorageService(storage_type='s3')
        service.s3_client = mock_s3_client
        
        # Mock public access failure
        with patch('backend.services.storage_service.requests.get') as mock_get:
            mock_get.side_effect = Exception("Public access failed")
            conversations = service._load_from_s3()
            
            assert len(conversations) == 1
            mock_s3_client.get_object.assert_called_once()

