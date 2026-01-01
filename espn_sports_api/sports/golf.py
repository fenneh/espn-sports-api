"""Golf API module."""

from __future__ import annotations

from typing import Any, Optional

from .base import BaseSport


class Golf(BaseSport):
    """Golf API access."""

    SPORT = "golf"
    LEAGUE = "pga"  # Default to PGA Tour

    TOURS = {
        "pga": "pga",
        "lpga": "lpga",
        "european": "eur",
        "champions": "champ",
    }

    def __init__(self, tour: str = "pga", client=None):
        """Initialize golf module.

        Args:
            tour: Tour code (e.g., 'pga', 'lpga', 'european').
            client: ESPN client instance.
        """
        super().__init__(client)
        self.LEAGUE = self.TOURS.get(tour.lower(), tour)

    def leaderboard(self, event_id: Optional[str] = None) -> dict[str, Any]:
        """Get tournament leaderboard.

        Args:
            event_id: Event ID. If not provided, gets current tournament.

        Returns:
            Leaderboard data.
        """
        params = {"event": event_id} if event_id else None
        return self.client.get(f"{self._endpoint()}/scoreboard", params)

    def rankings(self) -> dict[str, Any]:
        """Get world golf rankings.

        Returns:
            Rankings data.
        """
        return self.client.get_core(f"{self._core_endpoint()}/rankings")

    def schedule(self, season: Optional[int] = None) -> dict[str, Any]:
        """Get tournament schedule.

        Args:
            season: Season year.

        Returns:
            Schedule data.
        """
        params = {"season": season} if season else None
        return self.client.get_core(f"{self._core_endpoint()}/events", params)

    def player(self, player_id: str) -> dict[str, Any]:
        """Get golfer profile.

        Args:
            player_id: Player ID.

        Returns:
            Player data.
        """
        return self.athlete(player_id)
