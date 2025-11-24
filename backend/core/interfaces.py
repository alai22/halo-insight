"""
Service interfaces and abstract base classes

This module defines the contracts that services must implement,
enabling better testability and loose coupling.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Generator
from ..models.response import ClaudeResponse


class IStorageService(ABC):
    """Interface for storage services"""
    
    @abstractmethod
    def load_conversations(self) -> List[Dict[str, Any]]:
        """Load conversations from storage"""
        pass


class IClaudeService(ABC):
    """Interface for Claude API service"""
    
    @abstractmethod
    def send_message(self, 
                    message: str, 
                    model: str = None,
                    max_tokens: int = 1000,
                    system_prompt: Optional[str] = None) -> ClaudeResponse:
        """Send a message to Claude API"""
        pass
    
    @abstractmethod
    def stream_message(self, 
                      message: str, 
                      model: str = None,
                      max_tokens: int = 1000,
                      system_prompt: Optional[str] = None) -> Generator[Dict[str, Any], None, None]:
        """Stream a message from Claude API"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if Claude service is available"""
        pass


class IConversationService(ABC):
    """Interface for conversation data service"""
    
    @abstractmethod
    def load_conversations(self) -> None:
        """Load conversations from storage"""
        pass
    
    @abstractmethod
    def get_summary(self) -> Any:
        """Get conversation data summary"""
        pass
    
    @abstractmethod
    def search_conversations(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search conversations for specific content"""
        pass


class ICacheService(ABC):
    """Interface for cache services"""
    
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Get a value from cache"""
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set a value in cache with optional TTL (time to live in seconds)"""
        pass
    
    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete a key from cache"""
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clear all cache entries"""
        pass
    
    @abstractmethod
    def exists(self, key: str) -> bool:
        """Check if a key exists in cache"""
        pass



