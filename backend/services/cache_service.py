"""
In-memory cache service implementation

Provides fast, in-memory caching for single-instance deployments.
Cache is lost on application restart but provides excellent performance.
"""

import time
import hashlib
import json
from typing import Optional, Any, Dict
from ..utils.logging import get_logger
from ..core.interfaces import ICacheService

logger = get_logger('cache_service')


class InMemoryCacheService(ICacheService):
    """
    In-memory cache service with TTL (time-to-live) support.
    
    Suitable for single-instance deployments. Cache is lost on restart.
    """
    
    def __init__(self, default_ttl: int = 3600, max_size: Optional[int] = None):
        """
        Initialize in-memory cache service.
        
        Args:
            default_ttl: Default time-to-live in seconds (default: 1 hour)
            max_size: Maximum number of cache entries (None = unlimited)
        """
        self.cache: Dict[str, tuple[Any, float]] = {}  # key -> (value, expiry_time)
        self.default_ttl = default_ttl
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
        logger.info(f"In-memory cache initialized: default_ttl={default_ttl}s, max_size={max_size}")
    
    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """
        Generate a cache key from prefix and arguments.
        
        Args:
            prefix: Key prefix (e.g., 'claude:response')
            *args: Positional arguments to include in key
            **kwargs: Keyword arguments to include in key
            
        Returns:
            Cache key string
        """
        # Create a deterministic key from arguments
        key_parts = [prefix]
        
        # Add positional args
        for arg in args:
            if isinstance(arg, (str, int, float, bool)):
                key_parts.append(str(arg))
            else:
                # Hash complex objects
                key_parts.append(hashlib.md5(json.dumps(arg, sort_keys=True).encode()).hexdigest()[:8])
        
        # Add keyword args (sorted for consistency)
        if kwargs:
            sorted_kwargs = sorted(kwargs.items())
            for k, v in sorted_kwargs:
                if isinstance(v, (str, int, float, bool)):
                    key_parts.append(f"{k}:{v}")
                else:
                    key_parts.append(f"{k}:{hashlib.md5(json.dumps(v, sort_keys=True).encode()).hexdigest()[:8]}")
        
        return ":".join(key_parts)
    
    def _cleanup_expired(self) -> None:
        """Remove expired entries from cache"""
        current_time = time.time()
        expired_keys = [
            key for key, (_, expiry) in self.cache.items()
            if expiry < current_time
        ]
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            logger.debug(f"Cleaned up {len(expired_keys)} expired cache entries")
    
    def _evict_if_needed(self) -> None:
        """Evict oldest entries if cache exceeds max_size"""
        if self.max_size is None:
            return
        
        if len(self.cache) >= self.max_size:
            # Remove oldest entries (by expiry time, or FIFO)
            # Sort by expiry time and remove oldest
            sorted_items = sorted(
                self.cache.items(),
                key=lambda x: x[1][1]  # Sort by expiry time
            )
            # Remove 10% of entries
            num_to_remove = max(1, len(sorted_items) // 10)
            for key, _ in sorted_items[:num_to_remove]:
                del self.cache[key]
            logger.debug(f"Evicted {num_to_remove} cache entries (cache full)")
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found or expired
        """
        # Cleanup expired entries periodically (every 100 requests)
        if (self.hits + self.misses) % 100 == 0:
            self._cleanup_expired()
        
        if key in self.cache:
            value, expiry = self.cache[key]
            current_time = time.time()
            
            if current_time < expiry:
                self.hits += 1
                logger.debug(f"Cache HIT: {key}")
                return value
            else:
                # Expired, remove it
                del self.cache[key]
                logger.debug(f"Cache EXPIRED: {key}")
        
        self.misses += 1
        logger.debug(f"Cache MISS: {key}")
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Set a value in cache with optional TTL.
        
        Args:
            key: Cache key
            value: Value to cache (must be JSON-serializable)
            ttl: Time-to-live in seconds (None = use default_ttl)
        """
        ttl = ttl or self.default_ttl
        expiry_time = time.time() + ttl
        
        # Evict if needed before adding
        self._evict_if_needed()
        
        self.cache[key] = (value, expiry_time)
        logger.debug(f"Cache SET: {key} (ttl={ttl}s)")
    
    def delete(self, key: str) -> None:
        """
        Delete a key from cache.
        
        Args:
            key: Cache key to delete
        """
        if key in self.cache:
            del self.cache[key]
            logger.debug(f"Cache DELETE: {key}")
    
    def clear(self) -> None:
        """Clear all cache entries"""
        count = len(self.cache)
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        logger.info(f"Cache cleared: {count} entries removed")
    
    def exists(self, key: str) -> bool:
        """
        Check if a key exists in cache and is not expired.
        
        Args:
            key: Cache key to check
            
        Returns:
            True if key exists and is not expired, False otherwise
        """
        if key not in self.cache:
            return False
        
        _, expiry = self.cache[key]
        return time.time() < expiry
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        self._cleanup_expired()
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'size': len(self.cache),
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': round(hit_rate, 2),
            'max_size': self.max_size,
            'default_ttl': self.default_ttl
        }

