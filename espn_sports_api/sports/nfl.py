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

    def depth_charts(self, team_id: str) -> dict[str, Any]:
        """Get team depth chart.

        Args:
            team_id: Team ID.

        Returns:
            Depth chart data.
        """
        return self.client.get_core(f"{self._core_endpoint()}/teams/{team_id}/depthcharts")
