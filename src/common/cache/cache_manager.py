"""
Cache manager for caching computed results.
"""

import logging
import pickle
import hashlib
from typing import Any, Dict, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class CacheManager:
    """Manages caching of computed results."""
    
    def __init__(self, cache_dir: str = "data/cache"):
        """
        Initialize cache manager.
        
        Args:
            cache_dir: Cache directory path
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logger
    
    def _get_cache_key(self, key: str) -> str:
        """Generate cache key hash."""
        return hashlib.md5(key.encode()).hexdigest()
    
    def set(self, key: str, value: Any) -> bool:
        """
        Store value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            
        Returns:
            bool: Success status
        """
        try:
            cache_file = self.cache_dir / f"{self._get_cache_key(key)}.pkl"
            with open(cache_file, "wb") as f:
                pickle.dump(value, f)
            self.logger.debug(f"Cached: {key}")
            return True
        except Exception as e:
            self.logger.error(f"Cache write failed: {str(e)}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None
        """
        try:
            cache_file = self.cache_dir / f"{self._get_cache_key(key)}.pkl"
            if cache_file.exists():
                with open(cache_file, "rb") as f:
                    return pickle.load(f)
        except Exception as e:
            self.logger.error(f"Cache read failed: {str(e)}")
        return None
    
    def clear(self) -> bool:
        """Clear all cache."""
        try:
            for file in self.cache_dir.glob("*.pkl"):
                file.unlink()
            self.logger.info("Cache cleared")
            return True
        except Exception as e:
            self.logger.error(f"Cache clear failed: {str(e)}")
            return False
