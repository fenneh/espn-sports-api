"""WNBA API module."""

from typing import Any

from .base import BaseSport


class WNBA(BaseSport):
    """WNBA API access."""

    SPORT = "basketball"
    LEAGUE = "wnba"

    def draft(self, year: int = None) -> dict[str, Any]:
        """Get WNBA draft data.

        Args:
            year: Draft year.

        Returns:
            Draft data.
        """
        params = {"year": year} if year else None
        return self.client.get_core(f"{self._endpoint()}/draft", params)

    def leaders(self, category: str = None) -> dict[str, Any]:
        """Get statistical leaders.

        Args:
            category: Stat category.

        Returns:
            Leaders data.
        """
        endpoint = f"{self._endpoint()}/leaders"
        if category:
            endpoint = f"{endpoint}/{category}"
        return self.client.get_core(endpoint)

    def transactions(self) -> dict[str, Any]:
        """Get transactions.

        Returns:
            Transaction data.
        """
        return self.client.get_core(f"{self._endpoint()}/transactions")
