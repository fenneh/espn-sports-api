"""NHL API module."""

from __future__ import annotations

from typing import Any, Optional

from .base import BaseSport


class NHL(BaseSport):
    """NHL-specific API access."""

    SPORT = "hockey"
    LEAGUE = "nhl"

    def draft(self, year: Optional[int] = None) -> dict[str, Any]:
        """Get NHL draft data.

        Args:
            year: Draft year.

        Returns:
            Draft data.
        """
        params = {"year": year} if year else None
        return self.client.get_core(f"{self._core_endpoint()}/draft", params)

    def free_agents(self) -> dict[str, Any]:
        """Get free agents.

        Returns:
            Free agent data.
        """
        return self.client.get_core(f"{self._core_endpoint()}/freeagents")

    def transactions(self, limit: Optional[int] = None) -> dict[str, Any]:
        """Get transactions.

        Args:
            limit: Maximum number of results.

        Returns:
            Transaction data.
        """
        params = {"limit": limit} if limit else None
        return self.client.get_core(f"{self._core_endpoint()}/transactions", params)
