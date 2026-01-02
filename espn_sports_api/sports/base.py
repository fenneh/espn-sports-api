"""Base class for sport-specific modules."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any, Optional, Union

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
        """Build endpoint path for this sport (site API)."""
        base = f"{self.SPORT}/{self.LEAGUE}"
        return f"{base}/{path}" if path else base

    def _core_endpoint(self, path: str = "") -> str:
        """Build endpoint path for core API (uses /leagues/ format)."""
        base = f"{self.SPORT}/leagues/{self.LEAGUE}"
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
        return self.client.get_core(f"{self._core_endpoint()}/athletes", params)

    def athlete(self, athlete_id: str) -> dict[str, Any]:
        """Get athlete details.

        Args:
            athlete_id: Athlete ID.

        Returns:
            Athlete data.
        """
        return self.client.get_core(f"{self._core_endpoint()}/athletes/{athlete_id}")

    def athlete_stats(self, athlete_id: str) -> dict[str, Any]:
        """Get athlete statistics.

        Args:
            athlete_id: Athlete ID.

        Returns:
            Athlete stats.
        """
        return self.client.get_web(f"{self._core_endpoint()}/athletes/{athlete_id}/stats")

    def team_injuries(self, team_id: str) -> dict[str, Any]:
        """Get team injury report.

        Args:
            team_id: Team ID.

        Returns:
            Injury data.
        """
        return self.client.get_core(f"{self._core_endpoint()}/teams/{team_id}/injuries")

    def seasons(self, year: Optional[int] = None) -> dict[str, Any]:
        """Get season information.

        Args:
            year: Season year.

        Returns:
            Season data.
        """
        endpoint = f"{self._core_endpoint()}/seasons"
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
        return self.client.get_core(f"{self._core_endpoint()}/venues", params)

    def franchises(self) -> dict[str, Any]:
        """Get franchise information.

        Returns:
            Franchise history and metadata.
        """
        return self.client.get_core(f"{self._core_endpoint()}/franchises")

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
        return self.client.get_core(f"{self._core_endpoint()}/events", params or None)

    def playbyplay(self, event_id: str) -> dict[str, Any]:
        """Get play-by-play data for a game.

        Args:
            event_id: Event ID.

        Returns:
            Play-by-play data with drives and plays.
        """
        return self.client.get(f"{self._endpoint()}/summary", {"event": event_id})

    def box_score(self, event_id: str) -> dict[str, Any]:
        """Get box score for a game.

        Args:
            event_id: Event ID.

        Returns:
            Box score with team and player statistics.
        """
        return self.client.get(f"{self._endpoint()}/summary", {"event": event_id})

    def positions(self) -> dict[str, Any]:
        """Get all positions for this sport.

        Returns:
            Position data.
        """
        return self.client.get_core(f"{self._core_endpoint()}/positions")

    def leaders(self, category: Optional[str] = None) -> dict[str, Any]:
        """Get statistical leaders.

        Args:
            category: Stat category to filter by.

        Returns:
            Leaders data.
        """
        endpoint = f"{self._core_endpoint()}/leaders"
        if category:
            endpoint = f"{endpoint}/{category}"
        return self.client.get_core(endpoint)

    # -------------------------------------------------------------------------
    # Convenience methods for common operations
    # -------------------------------------------------------------------------

    def today(self) -> dict[str, Any]:
        """Get today's games.

        Returns:
            Scoreboard data for today.

        Example:
            >>> nfl = NFL()
            >>> games = nfl.today()
            >>> for event in games.get("events", []):
            ...     print(event["name"])
        """
        return self.scoreboard(dates=date.today().strftime("%Y%m%d"))

    def yesterday(self) -> dict[str, Any]:
        """Get yesterday's games.

        Returns:
            Scoreboard data for yesterday.
        """
        d = date.today() - timedelta(days=1)
        return self.scoreboard(dates=d.strftime("%Y%m%d"))

    def tomorrow(self) -> dict[str, Any]:
        """Get tomorrow's games.

        Returns:
            Scoreboard data for tomorrow.
        """
        d = date.today() + timedelta(days=1)
        return self.scoreboard(dates=d.strftime("%Y%m%d"))

    def on_date(self, d: Union[date, str]) -> dict[str, Any]:
        """Get games for a specific date.

        Args:
            d: A date object or string in YYYYMMDD format.

        Returns:
            Scoreboard data for the specified date.

        Example:
            >>> from datetime import date
            >>> nfl = NFL()
            >>> games = nfl.on_date(date(2024, 12, 25))
            >>> games = nfl.on_date("20241225")  # also works
        """
        if isinstance(d, date):
            d = d.strftime("%Y%m%d")
        return self.scoreboard(dates=d)

    def date_range(self, start: Union[date, str], end: Union[date, str]) -> dict[str, Any]:
        """Get games within a date range.

        Args:
            start: Start date (inclusive).
            end: End date (inclusive).

        Returns:
            Scoreboard data for the date range.

        Example:
            >>> from datetime import date
            >>> nfl = NFL()
            >>> games = nfl.date_range(date(2024, 12, 20), date(2024, 12, 31))
        """
        if isinstance(start, date):
            start = start.strftime("%Y%m%d")
        if isinstance(end, date):
            end = end.strftime("%Y%m%d")
        return self.scoreboard(dates=f"{start}-{end}")

    def live(self) -> dict[str, Any]:
        """Get currently live/in-progress games.

        Returns:
            Scoreboard data filtered to only in-progress games.

        Example:
            >>> nfl = NFL()
            >>> live_games = nfl.live()
            >>> print(f"{len(live_games['events'])} games in progress")
        """
        data = self.today()
        events = data.get("events", [])
        live_events = [
            e for e in events if e.get("status", {}).get("type", {}).get("state") == "in"
        ]
        return {**data, "events": live_events}

    def for_week(self, week_num: int, season: Optional[int] = None) -> dict[str, Any]:
        """Get games for a specific week (for weekly sports like NFL/NCAAF).

        Args:
            week_num: Week number (e.g., 1-18 for NFL regular season).
            season: Season year. Defaults to current season.

        Returns:
            Scoreboard data for the specified week.

        Example:
            >>> nfl = NFL()
            >>> week10 = nfl.for_week(10, 2024)
        """
        return self.scoreboard(week=week_num, season=season)

    def close(self) -> None:
        """Close client if we own it."""
        if self._owns_client:
            self.client.close()

    def __enter__(self) -> "BaseSport":
        return self

    def __exit__(self, *args) -> None:
        self.close()
