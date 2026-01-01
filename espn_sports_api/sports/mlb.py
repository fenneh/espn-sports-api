"""MLB API module."""

from __future__ import annotations

from typing import Any, Optional

from .base import BaseSport


class MLB(BaseSport):
    """MLB-specific API access."""

    SPORT = "baseball"
    LEAGUE = "mlb"

    def draft(self, year: Optional[int] = None) -> dict[str, Any]:
        """Get MLB draft data.

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
            category: Stat category (e.g., 'batting', 'pitching').

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

    def transactions(self, limit: Optional[int] = None) -> dict[str, Any]:
        """Get transactions.

        Args:
            limit: Max results (ignored, included for API compatibility).

        Returns:
            Transaction data.
        """
        return self.client.get_core(f"{self._core_endpoint()}/transactions")
