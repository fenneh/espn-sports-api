"""Racing API module (F1, NASCAR, IndyCar)."""

from typing import Any, Optional

from .base import BaseSport


class Racing(BaseSport):
    """Racing API access."""

    SPORT = "racing"
    LEAGUE = "f1"  # Default to Formula 1

    SERIES = {
        "f1": "f1",
        "formula1": "f1",
        "nascar": "nascar",
        "nascar_cup": "nascar",
        "indycar": "irl",
    }

    def __init__(self, series: str = "f1", client=None):
        """Initialize racing module.

        Args:
            series: Racing series code (e.g., 'f1', 'nascar', 'indycar').
            client: ESPN client instance.
        """
        super().__init__(client)
        self.LEAGUE = self.SERIES.get(series.lower(), series)

    def schedule(self, season: Optional[int] = None) -> dict[str, Any]:
        """Get race calendar.

        Args:
            season: Season year.

        Returns:
            Schedule data.
        """
        params = {"season": season} if season else None
        return self.client.get_core(f"{self._core_endpoint()}/events", params)

    def standings(self, season: Optional[int] = None, **kwargs) -> dict[str, Any]:
        """Get driver/constructor standings.

        Args:
            season: Season year.

        Returns:
            Standings data.
        """
        params = {"season": season} if season else None
        return self.client.get(f"{self._endpoint()}/standings", params)

    def results(self, event_id: str) -> dict[str, Any]:
        """Get race results.

        Args:
            event_id: Event ID.

        Returns:
            Race results.
        """
        return self.event(event_id)

    def driver(self, driver_id: str) -> dict[str, Any]:
        """Get driver profile.

        Args:
            driver_id: Driver ID.

        Returns:
            Driver data.
        """
        return self.athlete(driver_id)

    @classmethod
    def available_series(cls) -> dict[str, str]:
        """Get available racing series.

        Returns:
            Dictionary of friendly names to ESPN codes.
        """
        return cls.SERIES.copy()
