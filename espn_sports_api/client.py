"""Core ESPN API client."""

from __future__ import annotations

import hashlib
import json
import logging
import time
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .exceptions import (
    ESPNApiError,
    ESPNNotFoundError,
    ESPNRateLimitError,
    ESPNResponseError,
    ESPNServerError,
    ESPNTimeoutError,
)

logger = logging.getLogger(__name__)


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
                logger.debug("Cache hit (memory): %s", url)
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
                        logger.debug("Cache hit (disk): %s", url)
                        return cached["data"]
                    cache_file.unlink()
                except (json.JSONDecodeError, KeyError):
                    cache_file.unlink(missing_ok=True)

        logger.debug("Cache miss: %s", url)
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
    STANDINGS_URL = "https://site.api.espn.com/apis/v2/sports/"

    def __init__(
        self,
        timeout: int = 30,
        cache_ttl: Optional[int] = None,
        cache_dir: Optional[Path] = None,
        retries: int = 3,
    ):
        """Initialize the ESPN client.

        Args:
            timeout: Request timeout in seconds.
            cache_ttl: Cache time-to-live in seconds. None disables caching.
            cache_dir: Directory for disk cache. If None with cache_ttl set, uses memory only.
            retries: Number of retries for transient failures (429, 5xx). 0 disables.
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "espn-sports-api/0.4.0",
                "Accept": "application/json",
            }
        )

        if retries > 0:
            retry_strategy = Retry(
                total=retries,
                backoff_factor=0.5,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["GET"],
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            self.session.mount("https://", adapter)
            self.session.mount("http://", adapter)

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
            ESPNNotFoundError: If the resource is not found (404).
            ESPNRateLimitError: If rate limited (429).
            ESPNServerError: If the server returns a 5xx error.
            ESPNTimeoutError: If the request times out.
            ESPNResponseError: If the response is not valid JSON.
            ESPNApiError: For other HTTP errors.
        """
        url = urljoin(base_url, endpoint)

        # Check cache first
        if use_cache and self._cache:
            cached = self._cache.get(url, params)
            if cached is not None:
                return cached

        logger.debug("GET %s params=%s", url, params)

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
        except requests.Timeout as e:
            raise ESPNTimeoutError(f"Request timed out: {url}") from e
        except (requests.ConnectionError, ConnectionError) as e:
            raise ESPNApiError(f"Connection error: {url}") from e

        if not response.ok:
            self._raise_for_status(response)

        try:
            data = response.json()
        except ValueError as e:
            raise ESPNResponseError(f"Invalid JSON response from {url}") from e

        # Store in cache
        if use_cache and self._cache:
            self._cache.set(url, params, data)

        return data

    @staticmethod
    def _raise_for_status(response: requests.Response) -> None:
        """Raise an appropriate ESPNApiError for HTTP error responses."""
        code: int = response.status_code or 0
        msg = f"HTTP {code} for {response.url}"

        if code == 404:
            raise ESPNNotFoundError(msg)
        elif code == 429:
            raise ESPNRateLimitError(msg)
        elif 500 <= code < 600:
            raise ESPNServerError(msg, status_code=code)
        else:
            raise ESPNApiError(msg, status_code=code)

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

    def get_standings(self, endpoint: str, params: Optional[dict] = None) -> dict[str, Any]:
        """Make a request to the standings API (v2 sports endpoint).

        Args:
            endpoint: API endpoint path.
            params: Query parameters.

        Returns:
            JSON response.
        """
        return self._request(self.STANDINGS_URL, endpoint, params)

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
