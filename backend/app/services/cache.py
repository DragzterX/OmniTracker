import time
from typing import Any, Optional

class SimpleCache:
    """In-memory cache with time-to-live (TTL) to avoid external API rate limits."""
    
    def __init__(self, default_ttl: int = 600):
        self._cache: dict[str, tuple[float, Any]] = {}
        self._default_ttl = default_ttl

    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            expires_at, value = self._cache[key]
            if time.time() < expires_at:
                return value
            del self._cache[key]
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        duration = ttl if ttl is not None else self._default_ttl
        self._cache[key] = (time.time() + duration, value)

    def clear(self) -> None:
        self._cache.clear()

cache = SimpleCache()
