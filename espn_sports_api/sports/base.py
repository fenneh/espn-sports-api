"""Base class for sport-specific modules."""

from typing import Any, Optional

from ..client import ESPNClient


class BaseSport:
    """Base class for sport-specific API access."""

    SPORT: str = ""
    LEAGUE: str = ""

    def __init__(self, client: Optional[ESPNClient] = None):
        """Initialize sport module.

        Args:
            client: ESPN client instance. Creates new one if not provided.
        """
        self.client = client or ESPNClient()
        self._owns_client = client is None

    def _endpoint(self, path: str = "") -> str:
        """Build endpoint path for this sport."""
        base = f"{self.SPORT}/{self.LEAGUE}"
        return f"{base}/{path}" if path else base

    def scoreboard(
        self,
        dates: Optional[str] = None,
        limit: Optional[int] = None,
        groups: Optional[int] = None,
        calendar: bool = False,
        season: Optional[int] = None,
        seasontype: Optional[int] = None,
        week: Optional[int] = None,
    ) -> dict[str, Any]:
        """Get scoreboard data.

        Args:
            dates: Date filter (YYYYMMDD or YYYYMMDD-YYYYMMDD range).
            limit: Maximum number of results.
            groups: Conference/league group ID.
            calendar: Include calendar data.
            season: Season year (e.g., 2025).
            seasontype: Season type (1=preseason, 2=regular, 3=postseason, 4=offseason).
            week: Week number (1-18 for NFL regular season).

        Returns:
            Scoreboard data.
        """
        params = {}
        if dates:
            params["dates"] = dates
        if limit:
            params["limit"] = limit
        if groups:
            params["groups"] = groups
        if calendar:
            params["calendar"] = "true"
        if season:
            params["season"] = season
        if seasontype:
            params["seasontype"] = seasontype
        if week:
            params["week"] = week
        return self.client.get(f"{self._endpoint()}/scoreboard", params or None)

    def news(self, limit: Optional[int] = None) -> dict[str, Any]:
        """Get news articles.

        Args:
            limit: Maximum number of articles.

        Returns:
            News data.
        """
        params = {"limit": limit} if limit else None
        return self.client.get(f"{self._endpoint()}/news", params)

    def teams(self) -> dict[str, Any]:
        """Get all teams.

        Returns:
            Teams data.
        """
        return self.client.get(f"{self._endpoint()}/teams")

    def team(self, team_id: str) -> dict[str, Any]:
        """Get team details.

        Args:
            team_id: Team ID or abbreviation.

        Returns:
            Team data.
        """
        return self.client.get(f"{self._endpoint()}/teams/{team_id}")

    def team_roster(self, team_id: str) -> dict[str, Any]:
        """Get team roster.

        Args:
            team_id: Team ID or abbreviation.

        Returns:
            Roster data.
        """
        return self.client.get(f"{self._endpoint()}/teams/{team_id}/roster")

    def team_schedule(self, team_id: str, season: Optional[int] = None) -> dict[str, Any]:
        """Get team schedule.

        Args:
            team_id: Team ID or abbreviation.
            season: Season year.

        Returns:
            Schedule data.
        """
        params = {"season": season} if season else None
        return self.client.get(f"{self._endpoint()}/teams/{team_id}/schedule", params)

    def standings(
        self,
        season: Optional[int] = None,
        group: Optional[str] = None,
    ) -> dict[str, Any]:
        """Get standings.

        Args:
            season: Season year.
            group: Standings group (e.g., 'league', 'conference', 'division').

        Returns:
            Standings data.
        """
        params = {}
        if season:
            params["season"] = season
        if group:
            params["group"] = group
        return self.client.get(f"{self._endpoint()}/standings", params or None)

    def event(self, event_id: str) -> dict[str, Any]:
        """Get event/game details.

        Args:
            event_id: Event ID.

        Returns:
            Event data.
        """
        return self.client.get(f"{self._endpoint()}/summary", {"event": event_id})

    def athletes(self, limit: Optional[int] = None) -> dict[str, Any]:
        """Get athletes.

        Args:
            limit: Maximum number of results.

        Returns:
            Athletes data.
        """
        params = {"limit": limit} if limit else None
        return self.client.get_core(f"{self._endpoint()}/athletes", params)

    def athlete(self, athlete_id: str) -> dict[str, Any]:
        """Get athlete details.

        Args:
            athlete_id: Athlete ID.

        Returns:
            Athlete data.
        """
        return self.client.get_core(f"{self._endpoint()}/athletes/{athlete_id}")

    def athlete_stats(self, athlete_id: str) -> dict[str, Any]:
        """Get athlete statistics.

        Args:
            athlete_id: Athlete ID.

        Returns:
            Athlete stats.
        """
        return self.client.get_web(f"{self._endpoint()}/athletes/{athlete_id}/stats")

    def team_injuries(self, team_id: str) -> dict[str, Any]:
        """Get team injury report.

        Args:
            team_id: Team ID.

        Returns:
            Injury data.
        """
        return self.client.get_core(f"{self._endpoint()}/teams/{team_id}/injuries")

    def seasons(self, year: Optional[int] = None) -> dict[str, Any]:
        """Get season information.

        Args:
            year: Season year.

        Returns:
            Season data.
        """
        endpoint = f"{self._endpoint()}/seasons"
        if year:
            endpoint = f"{endpoint}/{year}"
        return self.client.get_core(endpoint)

    def injuries(self) -> dict[str, Any]:
        """Get league-wide injury report.

        Returns:
            All injuries across the league.
        """
        return self.client.get(f"{self._endpoint()}/injuries")

    def transactions(self, limit: Optional[int] = None) -> dict[str, Any]:
        """Get recent transactions (trades, signings, IR moves).

        Args:
            limit: Maximum number of results.

        Returns:
            Transaction data.
        """
        params = {"limit": limit} if limit else None
        return self.client.get(f"{self._endpoint()}/transactions", params)

    def statistics(self, category: Optional[str] = None) -> dict[str, Any]:
        """Get league statistics and leaders.

        Args:
            category: Stat category to filter by.

        Returns:
            Statistics data.
        """
        endpoint = f"{self._endpoint()}/statistics"
        if category:
            endpoint = f"{endpoint}/{category}"
        return self.client.get(endpoint)

    def venues(self, limit: Optional[int] = None) -> dict[str, Any]:
        """Get stadium/venue information.

        Args:
            limit: Maximum number of results.

        Returns:
            Venue data with capacity, location, indoor/outdoor.
        """
        params = {"limit": limit} if limit else None
        return self.client.get_core(f"{self._endpoint()}/venues", params)

    def franchises(self) -> dict[str, Any]:
        """Get franchise information.

        Returns:
            Franchise history and metadata.
        """
        return self.client.get_core(f"{self._endpoint()}/franchises")

    def events(
        self,
        dates: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> dict[str, Any]:
        """Get all events/games.

        Args:
            dates: Date filter (YYYYMMDD format).
            limit: Maximum number of results.

        Returns:
            Events data.
        """
        params = {}
        if dates:
            params["dates"] = dates
        if limit:
            params["limit"] = limit
        return self.client.get_core(f"{self._endpoint()}/events", params or None)

    def playbyplay(self, event_id: str) -> dict[str, Any]:
        """Get play-by-play data for a game.

        Args:
            event_id: Event ID.

        Returns:
            Play-by-play data with drives and plays.
        """
        return self.client.get(f"{self._endpoint()}/summary", {"event": event_id})

    def positions(self) -> dict[str, Any]:
        """Get all positions for this sport.

        Returns:
            Position data.
        """
        return self.client.get_core(f"{self._endpoint()}/positions")

    def leaders(self, category: Optional[str] = None) -> dict[str, Any]:
        """Get statistical leaders.

        Args:
            category: Stat category to filter by.

        Returns:
            Leaders data.
        """
        endpoint = f"{self._endpoint()}/leaders"
        if category:
            endpoint = f"{endpoint}/{category}"
        return self.client.get_core(endpoint)

    def close(self) -> None:
        """Close client if we own it."""
        if self._owns_client:
            self.client.close()

    def __enter__(self) -> "BaseSport":
        return self

    def __exit__(self, *args) -> None:
        self.close()
