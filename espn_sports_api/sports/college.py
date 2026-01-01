"""College sports API module."""

from __future__ import annotations

from typing import Any, Optional

from .base import BaseSport


class NCAAF(BaseSport):
    """NCAA Football API access."""

    SPORT = "football"
    LEAGUE = "college-football"

    def rankings(self) -> dict[str, Any]:
        """Get college football rankings (AP, Coaches poll).

        Returns:
            Rankings data.
        """
        return self.client.get(f"{self._endpoint()}/rankings")

    def conferences(self) -> dict[str, Any]:
        """Get conference information.

        Returns:
            Conference data.
        """
        return self.client.get_core(f"{self._core_endpoint()}/groups")

    def recruiting(self, year: Optional[int] = None) -> dict[str, Any]:
        """Get recruiting data.

        Args:
            year: Recruiting class year.

        Returns:
            Recruiting data.
        """
        params = {"year": year} if year else None
        return self.client.get_core(f"{self._core_endpoint()}/recruiting", params)


class NCAAB(BaseSport):
    """NCAA Basketball API access."""

    SPORT = "basketball"
    LEAGUE = "mens-college-basketball"

    def rankings(self) -> dict[str, Any]:
        """Get college basketball rankings (AP, Coaches poll).

        Returns:
            Rankings data.
        """
        return self.client.get(f"{self._endpoint()}/rankings")

    def conferences(self) -> dict[str, Any]:
        """Get conference information.

        Returns:
            Conference data.
        """
        return self.client.get_core(f"{self._core_endpoint()}/groups")

    def bracket(self, season: Optional[int] = None) -> dict[str, Any]:
        """Get NCAA tournament bracket.

        Args:
            season: Season year.

        Returns:
            Bracket data.
        """
        params = {"season": season} if season else None
        return self.client.get(f"{self._endpoint()}/tournament", params)

    def weeks(self, season: int, season_type: int = 2) -> dict[str, Any]:
        """Get weeks for a season.

        Args:
            season: Season year.
            season_type: Season type (2 = regular season).

        Returns:
            Week data.
        """
        return self.client.get_core(
            f"{self._core_endpoint()}/seasons/{season}/types/{season_type}/weeks"
        )


class WomensNCAAB(BaseSport):
    """NCAA Women's Basketball API access."""

    SPORT = "basketball"
    LEAGUE = "womens-college-basketball"

    def rankings(self) -> dict[str, Any]:
        """Get college basketball rankings.

        Returns:
            Rankings data.
        """
        return self.client.get(f"{self._endpoint()}/rankings")

    def bracket(self, season: Optional[int] = None) -> dict[str, Any]:
        """Get NCAA tournament bracket.

        Args:
            season: Season year.

        Returns:
            Bracket data.
        """
        params = {"season": season} if season else None
        return self.client.get(f"{self._endpoint()}/tournament", params)


class CollegeBaseball(BaseSport):
    """NCAA Baseball API access."""

    SPORT = "baseball"
    LEAGUE = "college-baseball"

    def rankings(self) -> dict[str, Any]:
        """Get college baseball rankings.

        Returns:
            Rankings data.
        """
        return self.client.get(f"{self._endpoint()}/rankings")

    def conferences(self) -> dict[str, Any]:
        """Get conference information.

        Returns:
            Conference data.
        """
        return self.client.get_core(f"{self._core_endpoint()}/groups")
