# Service Interface Implementation Plan

## Overview
Complete service interface implementation for all services to improve testability, enable implementation swapping, and provide clearer contracts.

## Current State

### ✅ Services with Interfaces (4/12)
- `IStorageService` → `StorageService`
- `IClaudeService` → `ClaudeService`
- `IConversationService` → `ConversationService`
- `ICacheService` → `InMemoryCacheService`

### ❌ Services Needing Interfaces (8/12)
- `RAGService`
- `SurvicateRAGService`
- `SurveyService`
- `GladlyDownloadService`
- `TopicExtractionService`
- `TopicStorageService`
- `AuthService`
- `SurvicateS3CacheService` (optional - internal utility)

## Implementation Plan

### Phase 1: Define Interfaces (backend/core/interfaces.py)

#### 1.1 IRAGService
```python
class IRAGService(ABC):
    @abstractmethod
    def process_query(self, question: str, model: str = None, max_tokens: int = 2000) -> Dict[str, Any]:
        """Process a RAG query and return analysis results"""
        pass
```

#### 1.2 ISurvicateRAGService
```python
class ISurvicateRAGService(ABC):
    @abstractmethod
    def process_query(self, question: str, model: str = None, max_tokens: int = 2000) -> Dict[str, Any]:
        """Process a RAG query for survey data and return analysis results"""
        pass
```

#### 1.3 ISurveyService
```python
class ISurveyService(ABC):
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
```

#### 1.4 IGladlyDownloadService
```python
class IGladlyDownloadService(ABC):
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
```

#### 1.5 ITopicExtractionService
```python
class ITopicExtractionService(ABC):
    @abstractmethod
    def extract_conversation_metadata(self, conversation_items: List[Dict], max_retries: int = 3) -> Dict[str, Any]:
        """Extract topic and metadata from a conversation using Claude API"""
        pass
```

#### 1.6 ITopicStorageService
```python
class ITopicStorageService(ABC):
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
```

#### 1.7 IAuthService
```python
class IAuthService(ABC):
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
```

### Phase 2: Update Service Implementations

#### 2.1 Update RAGService
- File: `backend/services/rag_service.py`
- Changes:
  - Import `IRAGService` from `..core.interfaces`
  - Change class declaration: `class RAGService(IRAGService):`
  - Ensure all abstract methods are implemented

#### 2.2 Update SurvicateRAGService
- File: `backend/services/survicate_rag_service.py`
- Changes:
  - Import `ISurvicateRAGService` from `..core.interfaces`
  - Change class declaration: `class SurvicateRAGService(ISurvicateRAGService):`
  - Ensure all abstract methods are implemented

#### 2.3 Update SurveyService
- File: `backend/services/survey_service.py`
- Changes:
  - Import `ISurveyService` from `..core.interfaces`
  - Change class declaration: `class SurveyService(ISurveyService):`
  - Ensure all abstract methods are implemented

#### 2.4 Update GladlyDownloadService
- File: `backend/services/gladly_download_service.py`
- Changes:
  - Import `IGladlyDownloadService` from `..core.interfaces`
  - Change class declaration: `class GladlyDownloadService(IGladlyDownloadService):`
  - Ensure all abstract methods are implemented

#### 2.5 Update TopicExtractionService
- File: `backend/services/topic_extraction_service.py`
- Changes:
  - Import `ITopicExtractionService` from `..core.interfaces`
  - Change class declaration: `class TopicExtractionService(ITopicExtractionService):`
  - Ensure all abstract methods are implemented

#### 2.6 Update TopicStorageService
- File: `backend/services/topic_storage_service.py`
- Changes:
  - Import `ITopicStorageService` from `..core.interfaces`
  - Change class declaration: `class TopicStorageService(ITopicStorageService):`
  - Ensure all abstract methods are implemented

#### 2.7 Update AuthService
- File: `backend/services/auth_service.py`
- Changes:
  - Import `IAuthService` from `..core.interfaces`
  - Change class declaration: `class AuthService(IAuthService):`
  - Ensure all abstract methods are implemented
  - Note: AuthService uses class methods - interface should reflect this

### Phase 3: Update Service Container

#### 3.1 Update Type Hints
- File: `backend/core/service_container.py`
- Changes:
  - Update TYPE_CHECKING imports to use interfaces instead of concrete classes
  - Update return types to use interfaces
  - Example:
    ```python
    from ..core.interfaces import (
        IRAGService, ISurvicateRAGService, ISurveyService,
        IGladlyDownloadService, ITopicExtractionService,
        ITopicStorageService, IAuthService
    )
    ```

#### 3.2 Update Service Container Methods
- Update all `get_*_service` methods to return interface types
- Example:
  ```python
  def get_rag_service(self, override: Optional['IRAGService'] = None) -> Optional['IRAGService']:
  ```

### Phase 4: Update Dependencies

#### 4.1 Update Services That Depend on Other Services
- Update constructor parameters to accept interface types
- Example: `TopicExtractionService` should accept `IClaudeService` instead of `ClaudeService`

#### 4.2 Update Route Handlers
- Ensure route handlers use service container methods (already done)
- No changes needed if using service container

### Phase 5: Testing & Validation

#### 5.1 Verify Interface Compliance
- Run type checker (mypy) if available
- Ensure all services implement their interfaces correctly

#### 5.2 Update Tests
- Update existing tests to use interface types
- Create mock implementations using interfaces

## Implementation Order

1. **Phase 1**: Define all interfaces in `backend/core/interfaces.py`
2. **Phase 2**: Update service implementations (can be done in parallel)
   - Start with leaf services (no dependencies): `AuthService`, `TopicStorageService`
   - Then services with simple dependencies: `TopicExtractionService`, `GladlyDownloadService`
   - Then services with complex dependencies: `RAGService`, `SurvicateRAGService`, `SurveyService`
3. **Phase 3**: Update service container
4. **Phase 4**: Update dependencies
5. **Phase 5**: Testing & validation

## Files to Modify

### Core Files
- `backend/core/interfaces.py` - Add 7 new interfaces
- `backend/core/service_container.py` - Update type hints and return types

### Service Files (8 files)
- `backend/services/rag_service.py`
- `backend/services/survicate_rag_service.py`
- `backend/services/survey_service.py`
- `backend/services/gladly_download_service.py`
- `backend/services/topic_extraction_service.py`
- `backend/services/topic_storage_service.py`
- `backend/services/auth_service.py`
- `backend/services/survicate_s3_cache_service.py` (optional)

### Dependency Updates
- Any service that instantiates other services directly should use service container or accept interfaces

## Benefits

1. **Better Testability**: Can easily create mock implementations
2. **Easier Implementation Swapping**: Can swap implementations without changing dependent code
3. **Clearer Contracts**: Interfaces document what each service must provide
4. **Type Safety**: Type checkers can verify interface compliance
5. **Consistency**: All services follow the same pattern

## Notes

- `AuthService` uses class methods - interface should use `@classmethod` or `@staticmethod` decorators
- Some services have internal/private methods that don't need to be in interfaces
- `SurvicateS3CacheService` is more of an internal utility - may not need an interface
- Consider if `SurveyParserService` needs an interface (currently seems like a utility)

## Estimated Effort

- **Phase 1**: 1-2 hours (defining interfaces)
- **Phase 2**: 2-3 hours (updating implementations)
- **Phase 3**: 1 hour (updating service container)
- **Phase 4**: 1-2 hours (updating dependencies)
- **Phase 5**: 1-2 hours (testing)

**Total**: ~6-10 hours

