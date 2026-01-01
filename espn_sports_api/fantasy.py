"""ESPN Fantasy Sports API module."""

from __future__ import annotations

from typing import Any, Optional

from .client import ESPNClient


class FantasyLeague:
    """ESPN Fantasy League access."""

    def __init__(
        self,
        sport: str,
        league_id: int,
        season: int,
        swid: Optional[str] = None,
        espn_s2: Optional[str] = None,
        client: Optional[ESPNClient] = None,
    ):
        """Initialize fantasy league access.

        Args:
            sport: Sport type ('ffl' for football, 'fba' for basketball, etc.).
            league_id: Fantasy league ID.
            season: Season year.
            swid: ESPN SWID cookie for private leagues.
            espn_s2: ESPN S2 cookie for private leagues.
            client: ESPN client instance.
        """
        self.sport = sport
        self.league_id = league_id
        self.season = season
        self.client = client or ESPNClient()
        self._owns_client = client is None

        if swid and espn_s2:
            self.client.session.cookies.set("SWID", swid)
            self.client.session.cookies.set("espn_s2", espn_s2)

    def _endpoint(self, path: str = "") -> str:
        """Build fantasy API endpoint."""
        base = f"games/{self.sport}/seasons/{self.season}/segments/0/leagues/{self.league_id}"
        return f"{base}/{path}" if path else base

    def info(self) -> dict[str, Any]:
        """Get league information.

        Returns:
            League info.
        """
        return self.client.get_fantasy(self._endpoint())

    def teams(self) -> dict[str, Any]:
        """Get league teams.

        Returns:
            Teams data.
        """
        return self.client.get_fantasy(self._endpoint(), {"view": "mTeam"})

    def roster(self, team_id: int) -> dict[str, Any]:
        """Get team roster.

        Args:
            team_id: Team ID.

        Returns:
            Roster data.
        """
        return self.client.get_fantasy(
            self._endpoint(),
            {"view": "mRoster", "forTeamId": team_id},
        )

    def matchups(self, week: Optional[int] = None) -> dict[str, Any]:
        """Get matchups.

        Args:
            week: Scoring period/week.

        Returns:
            Matchup data.
        """
        params = {"view": "mMatchup"}
        if week:
            params["scoringPeriodId"] = week
        return self.client.get_fantasy(self._endpoint(), params)

    def standings(self) -> dict[str, Any]:
        """Get league standings.

        Returns:
            Standings data.
        """
        return self.client.get_fantasy(self._endpoint(), {"view": "mStandings"})

    def free_agents(self, position: Optional[str] = None) -> dict[str, Any]:
        """Get available free agents.

        Args:
            position: Filter by position.

        Returns:
            Free agent data.
        """
        params = {"view": "kona_player_info"}
        if position:
            params["filterSlotIds"] = position
        return self.client.get_fantasy(self._endpoint(), params)

    def draft(self) -> dict[str, Any]:
        """Get draft results.

        Returns:
            Draft data.
        """
        return self.client.get_fantasy(self._endpoint(), {"view": "mDraftDetail"})

    def transactions(self) -> dict[str, Any]:
        """Get league transactions.

        Returns:
            Transaction data.
        """
        return self.client.get_fantasy(self._endpoint(), {"view": "mTransactions2"})

    def close(self) -> None:
        """Close client if we own it."""
        if self._owns_client:
            self.client.close()

    def __enter__(self) -> "FantasyLeague":
        return self

    def __exit__(self, *args) -> None:
        self.close()


class FantasyFootball(FantasyLeague):
    """ESPN Fantasy Football league."""

    def __init__(self, league_id: int, season: int, **kwargs):
        super().__init__("ffl", league_id, season, **kwargs)


class FantasyBasketball(FantasyLeague):
    """ESPN Fantasy Basketball league."""

    def __init__(self, league_id: int, season: int, **kwargs):
        super().__init__("fba", league_id, season, **kwargs)


class FantasyBaseball(FantasyLeague):
    """ESPN Fantasy Baseball league."""

    def __init__(self, league_id: int, season: int, **kwargs):
        super().__init__("flb", league_id, season, **kwargs)


class FantasyHockey(FantasyLeague):
    """ESPN Fantasy Hockey league."""

    def __init__(self, league_id: int, season: int, **kwargs):
        super().__init__("fhl", league_id, season, **kwargs)
