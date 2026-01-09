"""
Service Container for Dependency Injection

This container manages the lifecycle and dependencies of all services,
enabling dependency injection and making services easily testable.
"""

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    # Type hints only - avoids circular imports
    from ..core.interfaces import (
        ICacheService, IStorageService, IClaudeService, IConversationService,
        IRAGService, ISurvicateRAGService, IUnifiedRAGService, ISurveyService, 
        IGladlyDownloadService, IZoomDownloadService, ITopicExtractionService, 
        ITopicStorageService, IAuthService
    )

from ..utils.logging import get_logger

logger = get_logger('service_container')


class ServiceContainer:
    """
    Service container that manages service lifecycle and dependencies.
    
    This implements a singleton-like pattern where services are lazily
    initialized and cached. Services can be overridden for testing.
    """
    
    def __init__(self):
        """Initialize the service container"""
        # Core services - using interface types
        self._cache_service: Optional['ICacheService'] = None
        self._storage_service: Optional['IStorageService'] = None
        self._claude_service: Optional['IClaudeService'] = None
        self._conversation_service: Optional['IConversationService'] = None
        self._rag_service: Optional['IRAGService'] = None
        self._unified_rag_service: Optional['IUnifiedRAGService'] = None
        self._gladly_download_service: Optional['IGladlyDownloadService'] = None
        self._zoom_download_service: Optional['IZoomDownloadService'] = None
        self._survey_service: Optional['ISurveyService'] = None
        self._survicate_rag_service: Optional['ISurvicateRAGService'] = None
        self._analytics_service = None
        
        # Track if services are overridden (for testing)
        self._overrides: dict = {}
        
        logger.debug("Service container initialized")
    
    # Cache Service
    def get_cache_service(self, override: Optional['ICacheService'] = None) -> Optional['ICacheService']:
        """
        Get or create the CacheService instance.
        
        Args:
            override: Optional service instance to use instead (for testing)
            
        Returns:
            CacheService instance or None if caching is disabled
        """
        from ..utils.config import Config
        
        if not Config.CACHE_ENABLED:
            return None
        
        if override is not None:
            self._overrides['cache_service'] = override
            self._cache_service = override
            return override
        
        if 'cache_service' in self._overrides:
            return self._overrides.get('cache_service')
        
        if self._cache_service is None:
            # Lazy import to avoid circular dependencies
            from ..services.cache_service import InMemoryCacheService
            logger.debug("Creating InMemoryCacheService instance")
            self._cache_service = InMemoryCacheService(
                default_ttl=Config.CACHE_DEFAULT_TTL,
                max_size=Config.CACHE_MAX_SIZE
            )
            logger.info("Cache service initialized")
        
        return self._cache_service
    
    # Storage Service
    def get_storage_service(self, override: Optional['IStorageService'] = None) -> 'IStorageService':
        """
        Get or create the StorageService instance.
        
        Args:
            override: Optional service instance to use instead (for testing)
            
        Returns:
            StorageService instance
        """
        if override is not None:
            self._overrides['storage_service'] = override
            self._storage_service = override
            return override
        
        if 'storage_service' in self._overrides:
            return self._overrides['storage_service']
        
        if self._storage_service is None:
            # Lazy import to avoid circular dependencies
            from ..services.storage_service import StorageService
            logger.debug("Creating StorageService instance")
            self._storage_service = StorageService()
        
        return self._storage_service
    
    # Claude Service
    def get_claude_service(self, override: Optional['IClaudeService'] = None) -> Optional['IClaudeService']:
        """
        Get or create the ClaudeService instance.
        
        Args:
            override: Optional service instance to use instead (for testing)
            
        Returns:
            ClaudeService instance or None if initialization fails
        """
        if override is not None:
            self._overrides['claude_service'] = override
            self._claude_service = override
            return override
        
        if 'claude_service' in self._overrides:
            return self._overrides.get('claude_service')
        
        if self._claude_service is None:
            try:
                # Lazy import to avoid circular dependencies
                from ..services.claude_service import ClaudeService
                # Check API key status before attempting initialization
                from ..utils.config import Config
                api_key_status = Config.get_api_key_status()
                logger.debug(f"Attempting ClaudeService initialization - API key status: {api_key_status}")
                
                logger.debug("Creating ClaudeService instance")
                cache_service = self.get_cache_service()
                self._claude_service = ClaudeService(cache_service=cache_service)
                logger.debug("ClaudeService initialized")
            except ValueError as e:
                # ValueError means API key is missing - this is expected in some environments
                logger.warning(f"ClaudeService not initialized - API key not configured: {str(e)}")
                self._claude_service = None
            except Exception as e:
                # Other exceptions are unexpected
                logger.error(f"Failed to initialize ClaudeService: {str(e)}", exc_info=True)
                self._claude_service = None
        
        return self._claude_service
    
    # Conversation Service
    def get_conversation_service(self, override: Optional['IConversationService'] = None) -> 'IConversationService':
        """
        Get or create the ConversationService instance.
        
        Args:
            override: Optional service instance to use instead (for testing)
            
        Returns:
            ConversationService instance
        """
        if override is not None:
            self._overrides['conversation_service'] = override
            self._conversation_service = override
            return override
        
        if 'conversation_service' in self._overrides:
            return self._overrides['conversation_service']
        
        if self._conversation_service is None:
            # Lazy import to avoid circular dependencies
            from ..services.conversation_service import ConversationService
            logger.debug("Creating ConversationService instance")
            storage_service = self.get_storage_service()
            cache_service = self.get_cache_service()
            self._conversation_service = ConversationService(
                storage_service=storage_service,
                cache_service=cache_service
            )
        
        return self._conversation_service
    
    # RAG Service
    def get_rag_service(self, override: Optional['IRAGService'] = None) -> Optional['IRAGService']:
        """
        Get or create the RAGService instance.
        
        Requires ClaudeService and ConversationService to be available.
        
        Args:
            override: Optional service instance to use instead (for testing)
            
        Returns:
            RAGService instance or None if dependencies are unavailable
        """
        if override is not None:
            self._overrides['rag_service'] = override
            self._rag_service = override
            return override
        
        if 'rag_service' in self._overrides:
            return self._overrides.get('rag_service')
        
        if self._rag_service is None:
            # Lazy import to avoid circular dependencies
            from ..services.rag_service import RAGService
            claude_service = self.get_claude_service()
            if claude_service is None:
                logger.warning("RAGService not initialized - ClaudeService unavailable")
                return None
            
            conversation_service = self.get_conversation_service()
            logger.debug("Creating RAGService instance")
            self._rag_service = RAGService(claude_service, conversation_service)
        
        return self._rag_service
    
    # Unified RAG Service
    def get_unified_rag_service(self, override: Optional['IUnifiedRAGService'] = None) -> Optional['IUnifiedRAGService']:
        """
        Get or create the UnifiedRAGService instance.
        
        Requires ClaudeService, ConversationService, and SurveyService to be available.
        
        Args:
            override: Optional service instance to use instead (for testing)
            
        Returns:
            UnifiedRAGService instance or None if dependencies are unavailable
        """
        if override is not None:
            self._overrides['unified_rag_service'] = override
            self._unified_rag_service = override
            return override
        
        if 'unified_rag_service' in self._overrides:
            return self._overrides.get('unified_rag_service')
        
        if self._unified_rag_service is None:
            # Lazy import to avoid circular dependencies
            from ..services.unified_rag_service import UnifiedRAGService
            claude_service = self.get_claude_service()
            if claude_service is None:
                logger.warning("UnifiedRAGService not initialized - ClaudeService unavailable")
                return None
            
            conversation_service = self.get_conversation_service()
            survey_service = self.get_survey_service()
            # TODO: Add zoom service when available
            
            logger.debug("Creating UnifiedRAGService instance")
            self._unified_rag_service = UnifiedRAGService(
                claude_service=claude_service,
                conversation_service=conversation_service,
                survey_service=survey_service,
                zoom_service=None  # TODO: Add when available
            )
            logger.info("UnifiedRAGService initialized")
        
        return self._unified_rag_service
    
    # Gladly Download Service
    def get_gladly_download_service(self, override: Optional['IGladlyDownloadService'] = None) -> Optional['IGladlyDownloadService']:
        """
        Get or create the GladlyDownloadService instance.
        
        Args:
            override: Optional service instance to use instead (for testing)
            
        Returns:
            GladlyDownloadService instance or None if initialization fails
        """
        if override is not None:
            self._overrides['gladly_download_service'] = override
            self._gladly_download_service = override
            return override
        
        if 'gladly_download_service' in self._overrides:
            return self._overrides.get('gladly_download_service')
        
        if self._gladly_download_service is None:
            try:
                # Lazy import to avoid circular dependencies
                from ..services.gladly_download_service import GladlyDownloadService
                logger.debug("Creating GladlyDownloadService instance")
                self._gladly_download_service = GladlyDownloadService()
            except Exception as e:
                logger.error(f"Failed to initialize GladlyDownloadService: {str(e)}")
                self._gladly_download_service = None
        
        return self._gladly_download_service
    
    # Zoom Download Service
    def get_zoom_download_service(self, override: Optional['IZoomDownloadService'] = None) -> Optional['IZoomDownloadService']:
        """
        Get or create the ZoomDownloadService instance.
        
        Args:
            override: Optional service instance to use instead (for testing)
            
        Returns:
            ZoomDownloadService instance or None if initialization fails
        """
        if override is not None:
            self._overrides['zoom_download_service'] = override
            self._zoom_download_service = override
            return override
        
        if 'zoom_download_service' in self._overrides:
            return self._overrides.get('zoom_download_service')
        
        if self._zoom_download_service is None:
            try:
                # Lazy import to avoid circular dependencies
                from ..services.zoom_download_service import ZoomDownloadService
                logger.debug("Creating ZoomDownloadService instance")
                self._zoom_download_service = ZoomDownloadService()
            except Exception as e:
                logger.error(f"Failed to initialize ZoomDownloadService: {str(e)}")
                self._zoom_download_service = None
        
        return self._zoom_download_service
    
    # Survey Service
    def get_survey_service(self, override: Optional['ISurveyService'] = None) -> 'ISurveyService':
        """
        Get or create the SurveyService instance.
        
        Args:
            override: Optional service instance to use instead (for testing)
            
        Returns:
            SurveyService instance
        """
        if override is not None:
            self._overrides['survey_service'] = override
            self._survey_service = override
            return override
        
        if 'survey_service' in self._overrides:
            return self._overrides['survey_service']
        
        if self._survey_service is None:
            # Lazy import to avoid circular dependencies
            from ..services.survey_service import SurveyService
            logger.debug("Creating SurveyService instance")
            self._survey_service = SurveyService()
        
        return self._survey_service
    
    # Survicate RAG Service
    def get_survicate_rag_service(self, override: Optional['ISurvicateRAGService'] = None) -> Optional['ISurvicateRAGService']:
        """
        Get or create the SurvicateRAGService instance.
        
        Requires ClaudeService and SurveyService to be available.
        
        Args:
            override: Optional service instance to use instead (for testing)
            
        Returns:
            SurvicateRAGService instance or None if dependencies are unavailable
        """
        if override is not None:
            self._overrides['survicate_rag_service'] = override
            self._survicate_rag_service = override
            return override
        
        if 'survicate_rag_service' in self._overrides:
            return self._overrides.get('survicate_rag_service')
        
        if self._survicate_rag_service is None:
            # Lazy import to avoid circular dependencies
            from ..services.survicate_rag_service import SurvicateRAGService
            claude_service = self.get_claude_service()
            if claude_service is None:
                logger.warning("SurvicateRAGService not initialized - ClaudeService unavailable")
                return None
            
            survey_service = self.get_survey_service()
            logger.debug("Creating SurvicateRAGService instance")
            self._survicate_rag_service = SurvicateRAGService(claude_service, survey_service)
        
        return self._survicate_rag_service
    
    # Analytics Service
    def get_analytics_service(self, override=None):
        """
        Get or create the AnalyticsService instance.
        
        Args:
            override: Optional service instance to use instead (for testing)
            
        Returns:
            AnalyticsService instance
        """
        if override is not None:
            self._overrides['analytics_service'] = override
            self._analytics_service = override
            return override
        
        if 'analytics_service' in self._overrides:
            return self._overrides.get('analytics_service')
        
        if self._analytics_service is None:
            try:
                # Lazy import to avoid circular dependencies
                from ..services.analytics_service import AnalyticsService
                logger.debug("Creating AnalyticsService instance")
                self._analytics_service = AnalyticsService()
                logger.info("AnalyticsService initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize AnalyticsService: {str(e)}")
                self._analytics_service = None
        
        return self._analytics_service
    
    def clear_overrides(self):
        """Clear all service overrides (useful for testing cleanup)"""
        self._overrides.clear()
        logger.debug("Service overrides cleared")
    
    def reset(self):
        """Reset all services (for testing)"""
        self._cache_service = None
        self._storage_service = None
        self._claude_service = None
        self._conversation_service = None
        self._rag_service = None
        self._unified_rag_service = None
        self._gladly_download_service = None
        self._zoom_download_service = None
        self._survey_service = None
        self._survicate_rag_service = None
        self._analytics_service = None
        self._overrides.clear()
        logger.debug("Service container reset")

