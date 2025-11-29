"""
Custom exception hierarchy for structured error handling

All application errors should inherit from AppException to ensure
consistent error responses and better debugging.
"""

from typing import Dict, Optional


class AppException(Exception):
    """Base exception for all application errors"""
    status_code = 500
    error_code = "INTERNAL_ERROR"
    
    def __init__(self, message: str, details: Optional[Dict] = None):
        """
        Initialize application exception
        
        Args:
            message: Human-readable error message
            details: Optional dictionary with additional error context
        """
        self.message = message
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict:
        """Convert exception to dictionary for JSON response"""
        return {
            "code": self.error_code,
            "message": self.message,
            "details": self.details
        }


class ValidationError(AppException):
    """Input validation errors"""
    status_code = 400
    error_code = "VALIDATION_ERROR"


class NotFoundError(AppException):
    """Resource not found errors"""
    status_code = 404
    error_code = "NOT_FOUND"


class UnauthorizedError(AppException):
    """Authentication/authorization errors"""
    status_code = 401
    error_code = "UNAUTHORIZED"


class ServiceUnavailableError(AppException):
    """External service unavailable"""
    status_code = 503
    error_code = "SERVICE_UNAVAILABLE"


class ClaudeAPIError(AppException):
    """Claude API specific errors"""
    status_code = 502
    error_code = "CLAUDE_API_ERROR"


class RateLimitError(AppException):
    """Rate limit exceeded"""
    status_code = 429
    error_code = "RATE_LIMIT_EXCEEDED"


class ConfigurationError(AppException):
    """Configuration errors"""
    status_code = 500
    error_code = "CONFIGURATION_ERROR"


class TimeoutError(AppException):
    """Request timeout errors
    
    Note: This shadows Python's built-in TimeoutError, but provides
    better integration with our error handling system.
    """
    status_code = 504
    error_code = "TIMEOUT_ERROR"


class StorageError(AppException):
    """Storage operation errors"""
    status_code = 500
    error_code = "STORAGE_ERROR"

