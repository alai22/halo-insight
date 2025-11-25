"""
Configuration utilities
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration"""
    
    # API Configuration
    ANTHROPIC_API_KEY: Optional[str] = os.getenv('ANTHROPIC_API_KEY')
    # Default to claude-3-haiku-20240307 (verified working model)
    # Claude 4 models (claude-sonnet-4, claude-opus-4) may not be available with all API keys
    CLAUDE_MODEL: str = os.getenv('CLAUDE_MODEL', 'claude-3-haiku-20240307')
    CLAUDE_API_TIMEOUT: int = int(os.getenv('CLAUDE_API_TIMEOUT', '120'))  # Default 120 seconds for complex queries
    
    @classmethod
    def get_api_key_status(cls) -> dict:
        """Get status of API key for debugging"""
        key_present = cls.ANTHROPIC_API_KEY is not None
        key_length = len(cls.ANTHROPIC_API_KEY) if cls.ANTHROPIC_API_KEY else 0
        key_prefix = cls.ANTHROPIC_API_KEY[:12] + "..." if key_present and key_length > 12 else "N/A"
        return {
            'present': key_present,
            'length': key_length,
            'prefix': key_prefix
        }
    
    # Model aliases and fallbacks
    # Maps deprecated/unavailable models to working alternatives
    # Note: We don't alias Claude 4 models here - let them be tried first, fallback system handles failures
    MODEL_ALIASES = {
        # Legacy Claude 3.5 models (not available) -> map to working Claude 3
        'claude-3-5-sonnet': 'claude-3-haiku-20240307',
        'claude-3-5-sonnet-20241022': 'claude-3-haiku-20240307',
        'claude-3-5-sonnet-20240620': 'claude-3-haiku-20240307',
        'claude-3-5-haiku-20241022': 'claude-3-haiku-20240307',
        # Legacy Claude 3 models (deprecated/unavailable) -> map to working model
        'claude-3-opus-20240229': 'claude-3-haiku-20240307',
        'claude-3-sonnet-20240229': 'claude-3-haiku-20240307',  # Deprecated, use haiku
    }
    
    # List of verified working models (tested with current API key)
    # Ordered by preference for fallback - put verified working models first
    VERIFIED_MODELS = [
        'claude-3-haiku-20240307',  # Primary - verified working model
        'claude-3-sonnet-20240229',  # May work with some API keys
        'claude-sonnet-4',  # Try Claude 4 models last (may not be available)
        'claude-opus-4',   # Try Claude 4 models last (may not be available)
    ]
    
    # Fallback model if configured model doesn't work
    # Using Haiku as fallback (verified working, cost-effective)
    FALLBACK_MODEL = 'claude-3-haiku-20240307'
    
    @classmethod
    def resolve_model(cls, requested_model: Optional[str] = None) -> str:
        """
        Resolve a model name, applying aliases and fallbacks.
        
        Args:
            requested_model: The requested model name (or None to use default)
            
        Returns:
            A working model name
        """
        model = requested_model or cls.CLAUDE_MODEL
        
        # Check if it's an alias
        if model in cls.MODEL_ALIASES:
            logger = __import__('logging').getLogger('config')
            logger.info(f"Model alias '{model}' mapped to '{cls.MODEL_ALIASES[model]}'")
            return cls.MODEL_ALIASES[model]
        
        return model
    
    # Gladly API Configuration
    GLADLY_API_KEY: Optional[str] = os.getenv('GLADLY_API_KEY')
    GLADLY_AGENT_EMAIL: Optional[str] = os.getenv('GLADLY_AGENT_EMAIL')
    
    # Zoom API Configuration
    ZOOM_ACCOUNT_ID: Optional[str] = os.getenv('ZOOM_ACCOUNT_ID')
    ZOOM_CLIENT_ID: Optional[str] = os.getenv('ZOOM_CLIENT_ID')
    ZOOM_CLIENT_SECRET: Optional[str] = os.getenv('ZOOM_CLIENT_SECRET')
    
    # Storage Configuration
    STORAGE_TYPE: str = os.getenv('STORAGE_TYPE', 's3')
    S3_BUCKET_NAME: Optional[str] = os.getenv('S3_BUCKET_NAME')
    S3_FILE_KEY: str = os.getenv('S3_FILE_KEY', 'conversation_items.json')
    S3_REGION: str = os.getenv('S3_REGION', 'us-east-2')
    
    # Azure Storage Configuration
    AZURE_CONNECTION_STRING: Optional[str] = os.getenv('AZURE_CONNECTION_STRING')
    AZURE_CONTAINER_NAME: str = os.getenv('AZURE_CONTAINER_NAME', 'gladly-conversations')
    AZURE_BLOB_NAME: str = os.getenv('AZURE_BLOB_NAME', 'conversation_items.jsonl')
    
    # Flask Configuration
    FLASK_ENV: str = os.getenv('FLASK_ENV', 'production')
    FLASK_DEBUG: bool = os.getenv('FLASK_DEBUG', '0').lower() in ('true', '1', 'yes')
    FLASK_SECRET_KEY: Optional[str] = os.getenv('FLASK_SECRET_KEY')
    PORT: int = int(os.getenv('PORT', 5000))
    HOST: str = os.getenv('HOST', '0.0.0.0')
    
    # Local file fallback
    LOCAL_FILE_PATH: str = os.getenv('LOCAL_FILE_PATH', 'conversation_items.jsonl')
    
    # Survicate Survey Configuration
    # Use cleaned CSV with proper headers (single header row with Answer/Comment labels)
    SURVICATE_CSV_PATH: str = os.getenv('SURVICATE_CSV_PATH', 'data/survicate_cancelled_subscriptions_cleaned.csv')
    
    # Survicate API Configuration
    SURVICATE_API_KEY: Optional[str] = os.getenv('SURVICATE_API_KEY')
    SURVICATE_WORKSPACE_KEY: Optional[str] = os.getenv('SURVICATE_WORKSPACE_KEY')
    SURVICATE_WORKSPACE_ID: Optional[str] = os.getenv('SURVICATE_WORKSPACE_ID')
    SURVICATE_SURVEY_ID: str = os.getenv('SURVICATE_SURVEY_ID', 'e08c3365f14085e2')
    SURVICATE_API_BASE_URL: str = os.getenv('SURVICATE_API_BASE_URL', 'https://data-api.survicate.com/v2')
    
    # Survicate S3 Cache Configuration
    SURVICATE_CACHE_MAX_AGE_HOURS: int = int(os.getenv('SURVICATE_CACHE_MAX_AGE_HOURS', '24'))
    SURVICATE_S3_CACHE_KEY: str = os.getenv('SURVICATE_S3_CACHE_KEY', 'survicate-cache/api_responses.csv')
    SURVICATE_S3_AUGMENTED_CACHE_KEY: str = os.getenv('SURVICATE_S3_AUGMENTED_CACHE_KEY', 'survicate-cache/api_responses_augmented.csv')
    SURVICATE_S3_AUGMENTED_PREFIX: str = os.getenv('SURVICATE_S3_AUGMENTED_PREFIX', 'survicate-cache/augmented/')
    SURVICATE_S3_METADATA_KEY: str = os.getenv('SURVICATE_S3_METADATA_KEY', 'survicate-cache/api_cache_meta.json')
    SURVICATE_S3_AUGMENTED_METADATA_KEY: str = os.getenv('SURVICATE_S3_AUGMENTED_METADATA_KEY', 'survicate-cache/augmented_files_meta.json')
    
    # Survicate Chart Configuration
    SURVICATE_EXCLUDE_MONTHS: str = os.getenv('SURVICATE_EXCLUDE_MONTHS', '2024-11')  # Comma-separated list of year-month to exclude (e.g., '2024-11,2025-01')
    
    # Authentication Configuration
    # Password for password-based login (stored securely on backend)
    AUTH_PASSWORD: str = os.getenv('AUTH_PASSWORD', 'gladly2024')
    
    # PII Protection Configuration
    # Enable PII protection before sending data to Claude API
    # Options: 'hash' (deterministic hash), 'redact' ([REDACTED] placeholder), 'remove' (delete), 'none' (disabled)
    PII_REDACT_MODE: str = os.getenv('PII_REDACT_MODE', 'hash')
    # Preserve customer/conversation IDs (don't pseudonymize) - set to 'true' to preserve
    PII_PRESERVE_IDS: bool = os.getenv('PII_PRESERVE_IDS', 'false').lower() in ('true', '1', 'yes')
    # Enable name detection (may have false positives) - set to 'true' to enable
    PII_ENABLE_NAME_DETECTION: bool = os.getenv('PII_ENABLE_NAME_DETECTION', 'false').lower() in ('true', '1', 'yes')
    
    # Cache Configuration
    # Enable caching (set to 'false' to disable)
    CACHE_ENABLED: bool = os.getenv('CACHE_ENABLED', 'true').lower() in ('true', '1', 'yes')
    # Default TTL for cache entries in seconds (default: 1 hour)
    CACHE_DEFAULT_TTL: int = int(os.getenv('CACHE_DEFAULT_TTL', '3600'))
    # Maximum number of cache entries (None = unlimited)
    CACHE_MAX_SIZE: Optional[int] = int(os.getenv('CACHE_MAX_SIZE')) if os.getenv('CACHE_MAX_SIZE') else None
    # TTL for Claude API responses in seconds (default: 24 hours - Claude responses are expensive)
    CACHE_CLAUDE_TTL: int = int(os.getenv('CACHE_CLAUDE_TTL', '86400'))
    # TTL for conversation summaries in seconds (default: 1 hour)
    CACHE_SUMMARY_TTL: int = int(os.getenv('CACHE_SUMMARY_TTL', '3600'))
    # TTL for conversation search results in seconds (default: 30 minutes)
    CACHE_SEARCH_TTL: int = int(os.getenv('CACHE_SEARCH_TTL', '1800'))
    # Redis configuration (for future distributed caching)
    REDIS_HOST: Optional[str] = os.getenv('REDIS_HOST')
    REDIS_PORT: int = int(os.getenv('REDIS_PORT', '6379'))
    
    @classmethod
    def get_pii_config(cls) -> dict:
        """Get PII protection configuration"""
        return {
            'redact_mode': cls.PII_REDACT_MODE if cls.PII_REDACT_MODE != 'none' else None,
            'preserve_ids': cls.PII_PRESERVE_IDS,
            'enable_name_detection': cls.PII_ENABLE_NAME_DETECTION
        }
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration"""
        if not cls.ANTHROPIC_API_KEY:
            print("Warning: ANTHROPIC_API_KEY not set")
            return False
        
        if cls.STORAGE_TYPE == 's3' and not cls.S3_BUCKET_NAME:
            print("Warning: S3_BUCKET_NAME not set for S3 storage")
            return False
        
        if cls.STORAGE_TYPE == 'azure' and not cls.AZURE_CONNECTION_STRING:
            print("Warning: AZURE_CONNECTION_STRING not set for Azure storage")
            return False
        
        return True
