"""MLB API module."""

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
        return self.client.get_core(f"{self._endpoint()}/draft", params)

    def leaders(self, category: Optional[str] = None) -> dict[str, Any]:
        """Get statistical leaders.

        Args:
            category: Stat category (e.g., 'batting', 'pitching').

        Returns:
            Leaders data.
        """
        endpoint = f"{self._endpoint()}/leaders"
        if category:
            endpoint = f"{endpoint}/{category}"
        return self.client.get_core(endpoint)

    def free_agents(self) -> dict[str, Any]:
        """Get free agents.

        Returns:
            Free agent data.
        """
        return self.client.get_core(f"{self._endpoint()}/freeagents")

    def transactions(self) -> dict[str, Any]:
        """Get transactions.

        Returns:
            Transaction data.
        """
        return self.client.get_core(f"{self._endpoint()}/transactions")
