"""Core ESPN API client."""

from typing import Any, Optional
from urllib.parse import urljoin

import requests


class ESPNClient:
    """Base client for ESPN API requests."""

    BASE_URL = "https://site.api.espn.com/apis/site/v2/sports/"
    CORE_URL = "https://sports.core.api.espn.com/v2/sports/"
    WEB_URL = "https://site.web.api.espn.com/apis/common/v3/sports/"
    NOW_URL = "https://now.core.api.espn.com/v1/"
    FANTASY_URL = "https://lm-api-reads.fantasy.espn.com/apis/v3/"
    GAMBIT_URL = "https://gambit-api.fantasy.espn.com/apis/v1/"

    def __init__(self, timeout: int = 30):
        """Initialize the ESPN client.

        Args:
            timeout: Request timeout in seconds.
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "espn-sports-api/0.1.0",
                "Accept": "application/json",
            }
        )

    def _request(
        self,
        base_url: str,
        endpoint: str,
        params: Optional[dict] = None,
    ) -> dict[str, Any]:
        """Make an API request.

        Args:
            base_url: Base URL for the request.
            endpoint: API endpoint path.
            params: Query parameters.

        Returns:
            JSON response as dictionary.

        Raises:
            requests.HTTPError: If the request fails.
        """
        url = urljoin(base_url, endpoint)
        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

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

    def close(self) -> None:
        """Close the session."""
        self.session.close()

    def __enter__(self) -> "ESPNClient":
        return self

    def __exit__(self, *args) -> None:
        self.close()
