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

    def team_schedule(
        self,
        team_id: str,
        season: Optional[int] = None,
        fixtures: bool = False,
    ) -> dict[str, Any]:
        """Get team schedule.

        Args:
            team_id: Team ID.
            season: Season year.
            fixtures: If True, get upcoming fixtures. If False, get results.

        Returns:
            Schedule data.
        """
        params = {}
        if season:
            params["season"] = season
        if fixtures:
            params["fixture"] = "true"
        # Soccer uses 'all' league for team schedules
        return self.client.get(f"soccer/all/teams/{team_id}/schedule", params or None)

    @staticmethod
    def all_leagues_scoreboard(dates: Optional[str] = None) -> dict[str, Any]:
        """Get scoreboard across all leagues.

        Args:
            dates: Date filter (YYYYMMDD format).

        Returns:
            Scoreboard data from all leagues.
        """
        from ..client import ESPNClient

        client = ESPNClient()
        params = {"dates": dates} if dates else None
        return client.get("soccer/all/scoreboard", params)

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
