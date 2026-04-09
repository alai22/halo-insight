"""
Unit tests for custom exception hierarchy
"""

import pytest
from backend.core.exceptions import (
    AppException, ValidationError, NotFoundError, UnauthorizedError,
    ServiceUnavailableError, ClaudeAPIError, RateLimitError,
    ConfigurationError, TimeoutError, StorageError
)


class TestAppException:
    """Test base AppException class"""
    
    def test_app_exception_creation(self):
        """Test creating an AppException"""
        exc = AppException("Test error message")
        assert str(exc) == "Test error message"
        assert exc.message == "Test error message"
        assert exc.details == {}
        assert exc.status_code == 500
        assert exc.error_code == "INTERNAL_ERROR"
    
    def test_app_exception_with_details(self):
        """Test AppException with details"""
        details = {'field': 'test_field', 'value': 'test_value'}
        exc = AppException("Test error", details=details)
        assert exc.details == details
    
    def test_app_exception_to_dict(self):
        """Test converting AppException to dictionary"""
        exc = AppException("Test error", details={'field': 'test'})
        result = exc.to_dict()
        
        assert result == {
            'code': 'INTERNAL_ERROR',
            'message': 'Test error',
            'details': {'field': 'test'}
        }


class TestValidationError:
    """Test ValidationError exception"""
    
    def test_validation_error_properties(self):
        """Test ValidationError has correct properties"""
        exc = ValidationError("Invalid input")
        assert exc.status_code == 400
        assert exc.error_code == "VALIDATION_ERROR"
        assert exc.message == "Invalid input"
    
    def test_validation_error_to_dict(self):
        """Test ValidationError to_dict"""
        exc = ValidationError("Missing field", details={'field': 'email'})
        result = exc.to_dict()
        
        assert result == {
            'code': 'VALIDATION_ERROR',
            'message': 'Missing field',
            'details': {'field': 'email'}
        }


class TestNotFoundError:
    """Test NotFoundError exception"""
    
    def test_not_found_error_properties(self):
        """Test NotFoundError has correct properties"""
        exc = NotFoundError("Resource not found")
        assert exc.status_code == 404
        assert exc.error_code == "NOT_FOUND"
    
    def test_not_found_error_with_id(self):
        """Test NotFoundError with resource ID"""
        exc = NotFoundError("Conversation not found", details={'conversation_id': '123'})
        assert exc.details['conversation_id'] == '123'


class TestClaudeAPIError:
    """Test ClaudeAPIError exception"""
    
    def test_claude_api_error_properties(self):
        """Test ClaudeAPIError has correct properties"""
        exc = ClaudeAPIError("API request failed")
        assert exc.status_code == 502
        assert exc.error_code == "CLAUDE_API_ERROR"
    
    def test_claude_api_error_with_status_code(self):
        """Test ClaudeAPIError with HTTP status code"""
        exc = ClaudeAPIError("API error", details={'status_code': 500})
        assert exc.details['status_code'] == 500


class TestRateLimitError:
    """Test RateLimitError exception"""
    
    def test_rate_limit_error_properties(self):
        """Test RateLimitError has correct properties"""
        exc = RateLimitError("Rate limit exceeded")
        assert exc.status_code == 429
        assert exc.error_code == "RATE_LIMIT_EXCEEDED"


class TestTimeoutError:
    """Test TimeoutError exception"""
    
    def test_timeout_error_properties(self):
        """Test TimeoutError has correct properties"""
        exc = TimeoutError("Request timed out")
        assert exc.status_code == 504
        assert exc.error_code == "TIMEOUT_ERROR"
    
    def test_timeout_error_with_timeout_value(self):
        """Test TimeoutError with timeout details"""
        exc = TimeoutError("Request timed out", details={'timeout_seconds': 30})
        assert exc.details['timeout_seconds'] == 30


class TestConfigurationError:
    """Test ConfigurationError exception"""
    
    def test_configuration_error_properties(self):
        """Test ConfigurationError has correct properties"""
        exc = ConfigurationError("Missing API key")
        assert exc.status_code == 500
        assert exc.error_code == "CONFIGURATION_ERROR"


class TestStorageError:
    """Test StorageError exception"""
    
    def test_storage_error_properties(self):
        """Test StorageError has correct properties"""
        exc = StorageError("Storage operation failed")
        assert exc.status_code == 500
        assert exc.error_code == "STORAGE_ERROR"
    
    def test_storage_error_with_storage_type(self):
        """Test StorageError with storage type details"""
        exc = StorageError("S3 error", details={'storage_type': 's3', 'bucket': 'test-bucket'})
        assert exc.details['storage_type'] == 's3'
        assert exc.details['bucket'] == 'test-bucket'


class TestServiceUnavailableError:
    """Test ServiceUnavailableError exception"""
    
    def test_service_unavailable_error_properties(self):
        """Test ServiceUnavailableError has correct properties"""
        exc = ServiceUnavailableError("Service unavailable")
        assert exc.status_code == 503
        assert exc.error_code == "SERVICE_UNAVAILABLE"


class TestExceptionInheritance:
    """Test exception inheritance"""
    
    def test_all_exceptions_inherit_from_app_exception(self):
        """Test all custom exceptions inherit from AppException"""
        exceptions = [
            ValidationError("test"),
            NotFoundError("test"),
            UnauthorizedError("test"),
            ServiceUnavailableError("test"),
            ClaudeAPIError("test"),
            RateLimitError("test"),
            ConfigurationError("test"),
            TimeoutError("test"),
            StorageError("test")
        ]
        
        for exc in exceptions:
            assert isinstance(exc, AppException)
            assert isinstance(exc, Exception)
    
    def test_exception_to_dict_includes_all_fields(self):
        """Test that to_dict includes all required fields"""
        exc = ValidationError("Test message", details={'field': 'test'})
        result = exc.to_dict()
        
        assert 'code' in result
        assert 'message' in result
        assert 'details' in result
        assert len(result) == 3

