"""Core ESPN API client."""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urljoin

import requests


class Cache:
    """Simple cache for API responses."""

    def __init__(self, ttl: int = 300, cache_dir: Optional[Path] = None):
        """Initialize cache.

        Args:
            ttl: Time to live in seconds (default 5 minutes).
            cache_dir: Directory for disk cache. If None, uses memory only.
        """
        self.ttl = ttl
        self.cache_dir = cache_dir
        self._memory: dict[str, tuple[float, Any]] = {}

        if cache_dir:
            cache_dir.mkdir(parents=True, exist_ok=True)

    def _key(self, url: str, params: Optional[dict]) -> str:
        """Generate cache key from URL and params."""
        key_data = f"{url}:{json.dumps(params, sort_keys=True) if params else ''}"
        return hashlib.md5(key_data.encode()).hexdigest()

    def get(self, url: str, params: Optional[dict] = None) -> Optional[Any]:
        """Get cached response if valid."""
        key = self._key(url, params)
        now = time.time()

        # Check memory cache first
        if key in self._memory:
            timestamp, data = self._memory[key]
            if now - timestamp < self.ttl:
                return data
            del self._memory[key]

        # Check disk cache if enabled
        if self.cache_dir:
            cache_file = self.cache_dir / f"{key}.json"
            if cache_file.exists():
                try:
                    with open(cache_file) as f:
                        cached = json.load(f)
                    if now - cached["timestamp"] < self.ttl:
                        self._memory[key] = (cached["timestamp"], cached["data"])
                        return cached["data"]
                    cache_file.unlink()
                except (json.JSONDecodeError, KeyError):
                    cache_file.unlink(missing_ok=True)

        return None

    def set(self, url: str, params: Optional[dict], data: Any) -> None:
        """Store response in cache."""
        key = self._key(url, params)
        now = time.time()

        self._memory[key] = (now, data)

        if self.cache_dir:
            cache_file = self.cache_dir / f"{key}.json"
            with open(cache_file, "w") as f:
                json.dump({"timestamp": now, "data": data}, f)

    def clear(self) -> None:
        """Clear all cached data."""
        self._memory.clear()

        if self.cache_dir:
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()


class ESPNClient:
    """Base client for ESPN API requests."""

    BASE_URL = "https://site.api.espn.com/apis/site/v2/sports/"
    CORE_URL = "https://sports.core.api.espn.com/v2/sports/"
    WEB_URL = "https://site.web.api.espn.com/apis/common/v3/sports/"
    NOW_URL = "https://now.core.api.espn.com/v1/"
    FANTASY_URL = "https://lm-api-reads.fantasy.espn.com/apis/v3/"
    GAMBIT_URL = "https://gambit-api.fantasy.espn.com/apis/v1/"

    def __init__(
        self,
        timeout: int = 30,
        cache_ttl: Optional[int] = None,
        cache_dir: Optional[Path] = None,
    ):
        """Initialize the ESPN client.

        Args:
            timeout: Request timeout in seconds.
            cache_ttl: Cache time-to-live in seconds. None disables caching.
            cache_dir: Directory for disk cache. If None with cache_ttl set, uses memory only.
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "espn-sports-api/0.2.0",
                "Accept": "application/json",
            }
        )

        # Initialize cache if TTL is provided
        self._cache: Optional[Cache] = None
        if cache_ttl is not None:
            self._cache = Cache(ttl=cache_ttl, cache_dir=cache_dir)

    def _request(
        self,
        base_url: str,
        endpoint: str,
        params: Optional[dict] = None,
        use_cache: bool = True,
    ) -> dict[str, Any]:
        """Make an API request.

        Args:
            base_url: Base URL for the request.
            endpoint: API endpoint path.
            params: Query parameters.
            use_cache: Whether to use cache for this request.

        Returns:
            JSON response as dictionary.

        Raises:
            requests.HTTPError: If the request fails.
        """
        url = urljoin(base_url, endpoint)

        # Check cache first
        if use_cache and self._cache:
            cached = self._cache.get(url, params)
            if cached is not None:
                return cached

        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()

        # Store in cache
        if use_cache and self._cache:
            self._cache.set(url, params, data)

        return data

    def get(self, endpoint: str, params: Optional[dict] = None) -> dict[str, Any]:
        """Make a request to the site API.

        Args:
            endpoint: API endpoint path.
            params: Query parameters.

        Returns:
            JSON response.
        """
        return self._request(self.BASE_URL, endpoint, params)

    def get_core(self, endpoint: str, params: Optional[dict] = None) -> dict[str, Any]:
        """Make a request to the core API.

        Args:
            endpoint: API endpoint path.
            params: Query parameters.

        Returns:
            JSON response.
        """
        return self._request(self.CORE_URL, endpoint, params)

    def get_now(self, endpoint: str, params: Optional[dict] = None) -> dict[str, Any]:
        """Make a request to the now API.

        Args:
            endpoint: API endpoint path.
            params: Query parameters.

        Returns:
            JSON response.
        """
        return self._request(self.NOW_URL, endpoint, params)

    def get_fantasy(self, endpoint: str, params: Optional[dict] = None) -> dict[str, Any]:
        """Make a request to the fantasy API.

        Args:
            endpoint: API endpoint path.
            params: Query parameters.

        Returns:
            JSON response.
        """
        return self._request(self.FANTASY_URL, endpoint, params)

    def get_web(self, endpoint: str, params: Optional[dict] = None) -> dict[str, Any]:
        """Make a request to the web API (athlete stats).

        Args:
            endpoint: API endpoint path.
            params: Query parameters.

        Returns:
            JSON response.
        """
        return self._request(self.WEB_URL, endpoint, params)

    def get_gambit(self, endpoint: str, params: Optional[dict] = None) -> dict[str, Any]:
        """Make a request to the gambit API (pick'em challenges).

        Args:
            endpoint: API endpoint path.
            params: Query parameters.

        Returns:
            JSON response.
        """
        return self._request(self.GAMBIT_URL, endpoint, params)

    def clear_cache(self) -> None:
        """Clear all cached responses."""
        if self._cache:
            self._cache.clear()

    def close(self) -> None:
        """Close the session."""
        self.session.close()

    def __enter__(self) -> "ESPNClient":
        return self

    def __exit__(self, *args) -> None:
        self.close()
