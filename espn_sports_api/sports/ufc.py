"""UFC/MMA API module."""

from typing import Any, Optional

from .base import BaseSport


class UFC(BaseSport):
    """UFC/MMA API access."""

    SPORT = "mma"
    LEAGUE = "ufc"

    def rankings(self, division: Optional[str] = None) -> dict[str, Any]:
        """Get UFC rankings.

        Args:
            division: Weight division (e.g., 'lightweight', 'heavyweight').

        Returns:
            Rankings data.
        """
        endpoint = f"{self._endpoint()}/rankings"
        if division:
            endpoint = f"{endpoint}/{division}"
        return self.client.get_core(endpoint)

    def events(self, limit: Optional[int] = None) -> dict[str, Any]:
        """Get upcoming UFC events.

        Args:
            limit: Maximum number of events.

        Returns:
            Events data.
        """
        params = {"limit": limit} if limit else None
        return self.client.get_core(f"{self._endpoint()}/events", params)

    def event_details(self, event_id: str) -> dict[str, Any]:
        """Get UFC event details including fight card.

        Args:
            event_id: Event ID.

        Returns:
            Event details.
        """
        return self.client.get_core(f"{self._endpoint()}/events/{event_id}")

    def fighter(self, fighter_id: str) -> dict[str, Any]:
        """Get fighter profile.

        Args:
            fighter_id: Fighter ID.

        Returns:
            Fighter data.
        """
        return self.athlete(fighter_id)
