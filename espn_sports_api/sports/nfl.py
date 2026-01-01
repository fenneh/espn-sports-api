"""NFL API module."""

from __future__ import annotations

from typing import Any, Optional

from .base import BaseSport


class NFL(BaseSport):
    """NFL-specific API access."""

    SPORT = "football"
    LEAGUE = "nfl"

    def draft(self, year: Optional[int] = None) -> dict[str, Any]:
        """Get NFL draft data.

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
            category: Stat category (e.g., 'passing', 'rushing', 'receiving').

        Returns:
            Leaders data.
        """
        endpoint = f"{self._core_endpoint()}/leaders"
        if category:
            endpoint = f"{endpoint}/{category}"
        return self.client.get_core(endpoint)

    def injuries(self) -> dict[str, Any]:
        """Get league-wide injury reports.

        Returns:
            Injury data.
        """
        # Use site API for injuries as core API doesn't support league-wide
        return self.client.get(f"{self._endpoint()}/injuries")

    def depth_charts(self, team_id: str) -> dict[str, Any]:
        """Get team depth chart.

        Args:
            team_id: Team ID.

        Returns:
            Depth chart data.
        """
        return self.client.get_core(f"{self._core_endpoint()}/teams/{team_id}/depthcharts")
