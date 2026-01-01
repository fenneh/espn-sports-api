"""Tennis API module."""

from typing import Any, Optional

from .base import BaseSport


class Tennis(BaseSport):
    """Tennis API access."""

    SPORT = "tennis"
    LEAGUE = "atp"  # Default to ATP

    TOURS = {
        "atp": "atp",
        "wta": "wta",
    }

    def __init__(self, tour: str = "atp", client=None):
        """Initialize tennis module.

        Args:
            tour: Tour code ('atp' or 'wta').
            client: ESPN client instance.
        """
        super().__init__(client)
        self.LEAGUE = self.TOURS.get(tour.lower(), tour)

    def rankings(self) -> dict[str, Any]:
        """Get tennis rankings.

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

    def tournament(self, event_id: str) -> dict[str, Any]:
        """Get tournament details.

        Args:
            event_id: Event ID.

        Returns:
            Tournament data.
        """
        return self.event(event_id)

    def player(self, player_id: str) -> dict[str, Any]:
        """Get player profile.

        Args:
            player_id: Player ID.

        Returns:
            Player data.
        """
        return self.athlete(player_id)
