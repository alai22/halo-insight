"""
Service interfaces and abstract base classes

This module defines the contracts that services must implement,
enabling better testability and loose coupling.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Generator, Callable, Union
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


class IRAGService(ABC):
    """Interface for RAG (Retrieval-Augmented Generation) service"""
    
    @abstractmethod
    def process_query(self, question: str, model: str = None, max_tokens: int = 2000) -> Dict[str, Any]:
        """Process a RAG query and return analysis results"""
        pass


class ISurvicateRAGService(ABC):
    """Interface for Survicate RAG service"""
    
    @abstractmethod
    def process_query(self, question: str, model: str = None, max_tokens: int = 2000) -> Dict[str, Any]:
        """Process a RAG query for survey data and return analysis results"""
        pass


class ISurveyService(ABC):
    """Interface for survey data service"""
    
    @abstractmethod
    def load_surveys(self, data_source: Optional[str] = None) -> None:
        """Load surveys from specified source"""
        pass
    
    @abstractmethod
    def get_summary(self) -> Any:
        """Get survey data summary"""
        pass
    
    @abstractmethod
    def search_surveys(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search surveys for specific content"""
        pass
    
    @abstractmethod
    def semantic_search_surveys(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Semantic search surveys using embeddings"""
        pass
    
    @abstractmethod
    def get_surveys_by_date_range(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get surveys within a date range"""
        pass
    
    @abstractmethod
    def refresh_surveys(self, data_source: Optional[str] = None) -> None:
        """Refresh surveys from specified source"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if survey service is available"""
        pass


class IGladlyDownloadService(ABC):
    """Interface for Gladly download service"""
    
    @abstractmethod
    def download_conversation_items(self, conversation_id: str) -> Optional[Dict]:
        """Download conversation items for a specific conversation ID"""
        pass
    
    @abstractmethod
    def download_batch(self, csv_file: str, output_file: str = None, 
                      max_duration_minutes: int = 30, batch_size: int = 500,
                      start_date: str = None, end_date: str = None,
                      progress_callback: Optional[Callable] = None) -> None:
        """Download conversations in batches with time limit"""
        pass
    
    @abstractmethod
    def read_conversation_ids_from_csv(self, csv_file: str) -> List[str]:
        """Read conversation IDs from CSV file"""
        pass
    
    @abstractmethod
    def filter_conversations_by_date(self, csv_file: str, conversation_ids: List[str], 
                                   start_date: str, end_date: str) -> List[str]:
        """Filter conversation IDs by date range"""
        pass
    
    @abstractmethod
    def get_processed_ids(self, output_file: str) -> set:
        """Get set of already processed conversation IDs"""
        pass


class ITopicExtractionService(ABC):
    """Interface for topic extraction service"""
    
    @abstractmethod
    def extract_conversation_metadata(self, conversation_items: List[Dict], max_retries: int = 3) -> Dict[str, Any]:
        """Extract topic and metadata from a conversation using Claude API"""
        pass


class ITopicStorageService(ABC):
    """Interface for topic storage service"""
    
    @abstractmethod
    def save_topics_for_date(self, date: str, topic_mapping: Dict[str, Union[str, Dict[str, Any]]]) -> None:
        """Save topics for a specific date"""
        pass
    
    @abstractmethod
    def add_topic_for_date(self, date: str, conversation_id: str, 
                          topic_or_metadata: Union[str, Dict[str, Any]], 
                          save_immediately: bool = False) -> None:
        """Add a topic for a specific conversation on a date"""
        pass
    
    @abstractmethod
    def get_topics_for_date(self, date: str) -> Optional[Dict[str, Union[str, Dict[str, Any]]]]:
        """Get all topics for a specific date"""
        pass
    
    @abstractmethod
    def get_topics_only_for_date(self, date: str) -> Optional[Dict[str, str]]:
        """Get topics only (without metadata) for a specific date"""
        pass
    
    @abstractmethod
    def get_extraction_status(self) -> Dict[str, Dict[str, int]]:
        """Get status of extracted topics by date"""
        pass
    
    @abstractmethod
    def has_topics_for_date(self, date: str) -> bool:
        """Check if topics exist for a date"""
        pass
    
    @abstractmethod
    def save_topics_incremental(self, date: str, save_every: int = 10) -> None:
        """Save topics incrementally during batch processing"""
        pass


class IAuthService(ABC):
    """Interface for authentication service
    
    Note: Implementations should use class methods for these methods.
    """
    
    @abstractmethod
    def validate_email_domain(self, email: str) -> bool:
        """Validate email domain against allowed list"""
        pass
    
    @abstractmethod
    def generate_token(self, email: str) -> str:
        """Generate authentication token for email"""
        pass
    
    @abstractmethod
    def verify_token(self, token: str) -> Optional[str]:
        """Verify token and return email if valid"""
        pass
    
    @abstractmethod
    def revoke_token(self, token: str) -> bool:
        """Revoke a token"""
        pass
    
    @abstractmethod
    def get_token_count(self) -> int:
        """Get current number of active tokens"""
        pass


