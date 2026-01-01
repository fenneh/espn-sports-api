"""NBA API module."""

from __future__ import annotations

from typing import Any, Optional

from .base import BaseSport


class NBA(BaseSport):
    """NBA-specific API access."""

    SPORT = "basketball"
    LEAGUE = "nba"

    def draft(self, year: Optional[int] = None) -> dict[str, Any]:
        """Get NBA draft data.

        Args:
            year: Draft year.

        Returns:
            Draft data.
        """
        params = {"year": year} if year else None
        return self.client.get_core(f"{self._core_endpoint()}/draft", params)

    def leaders(self, category: Optional[str] = None) -> dict[str, Any]:
        """Get statistical leaders.

        Args:
            category: Stat category (e.g., 'points', 'rebounds', 'assists').

        Returns:
            Leaders data.
        """
        endpoint = f"{self._core_endpoint()}/leaders"
        if category:
            endpoint = f"{endpoint}/{category}"
        return self.client.get_core(endpoint)

    def free_agents(self) -> dict[str, Any]:
        """Get free agents.

        Returns:
            Free agent data.
        """
        return self.client.get_core(f"{self._core_endpoint()}/freeagents")

    def transactions(self) -> dict[str, Any]:
        """Get transactions.

        Returns:
            Transaction data.
        """
        return self.client.get_core(f"{self._core_endpoint()}/transactions")
