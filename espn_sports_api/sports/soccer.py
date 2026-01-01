"""Soccer API module."""

from typing import Any, Optional

from .base import BaseSport


class Soccer(BaseSport):
    """Soccer/Football API access."""

    SPORT = "soccer"
    LEAGUE = "eng.1"  # Default to Premier League

    # Common league codes
    LEAGUES = {
        "epl": "eng.1",
        "premier_league": "eng.1",
        "championship": "eng.2",
        "la_liga": "esp.1",
        "bundesliga": "ger.1",
        "serie_a": "ita.1",
        "ligue_1": "fra.1",
        "mls": "usa.1",
        "champions_league": "uefa.champions",
        "europa_league": "uefa.europa",
        "world_cup": "fifa.world",
    }

    def __init__(self, league: str = "epl", client=None):
        """Initialize soccer module.

        Args:
            league: League code (e.g., 'epl', 'la_liga') or ESPN code (e.g., 'eng.1').
            client: ESPN client instance.
        """
        super().__init__(client)
        self.LEAGUE = self.LEAGUES.get(league.lower(), league)

    def scoreboard(
        self,
        dates: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> dict[str, Any]:
        """Get scoreboard data.

        Args:
            dates: Date filter (YYYYMMDD format).
            limit: Maximum number of results.

        Returns:
            Scoreboard data.
        """
        params = {}
        if dates:
            params["dates"] = dates
        if limit:
            params["limit"] = limit
        return self.client.get(f"{self._endpoint()}/scoreboard", params or None)

    def table(self) -> dict[str, Any]:
        """Get league table/standings.

        Returns:
            League table data.
        """
        return self.standings()

    def transfers(self) -> dict[str, Any]:
        """Get transfer news.

        Returns:
            Transfer data.
        """
        return self.client.get_core(f"{self._endpoint()}/transfers")

    @classmethod
    def available_leagues(cls) -> dict[str, str]:
        """Get available league codes.

        Returns:
            Dictionary of friendly names to ESPN codes.
        """
        return cls.LEAGUES.copy()
