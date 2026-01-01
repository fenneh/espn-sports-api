"""Betting odds extraction utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Spread:
    """Point spread data."""

    favorite: str
    spread: float
    favorite_odds: int
    underdog_odds: int
    provider: str


@dataclass
class Moneyline:
    """Moneyline odds data."""

    home_team: str
    away_team: str
    home_odds: int
    away_odds: int
    provider: str


@dataclass
class Total:
    """Over/under total data."""

    over_under: float
    over_odds: int
    under_odds: int
    provider: str


@dataclass
class GameOdds:
    """Complete odds for a game."""

    event_id: str
    home_team: str
    away_team: str
    spread: Optional[Spread] = None
    moneyline: Optional[Moneyline] = None
    total: Optional[Total] = None


class Odds:
    """Extract betting data from ESPN API responses."""

    @staticmethod
    def from_event(event: dict[str, Any]) -> Optional[GameOdds]:
        """Extract odds from an event/game.

        Args:
            event: Event data from scoreboard response.

        Returns:
            GameOdds object or None if no odds available.
        """
        competitions = event.get("competitions", [])
        if not competitions:
            return None

        competition = competitions[0]
        odds_list = competition.get("odds", [])
        if not odds_list:
            return None

        competitors = competition.get("competitors", [])
        home_team = ""
        away_team = ""
        for comp in competitors:
            if comp.get("homeAway") == "home":
                home_team = comp.get("team", {}).get("displayName", "")
            else:
                away_team = comp.get("team", {}).get("displayName", "")

        odds_data = odds_list[0]
        provider = odds_data.get("provider", {}).get("name", "Unknown")

        spread = None
        if "spread" in odds_data:
            spread_val = odds_data.get("spread", 0)
            ps = odds_data.get("pointSpread", {})
            details = odds_data.get("details", "")
            favorite = details.split()[0] if details else ""
            ps_american = ps.get("american", {}) if ps else {}
            spread = Spread(
                favorite=favorite,
                spread=abs(float(spread_val)) if spread_val else 0,
                favorite_odds=ps_american.get("favorite", {}).get("close", 0),
                underdog_odds=ps_american.get("underdog", {}).get("close", 0),
                provider=provider,
            )

        moneyline = None
        ml = odds_data.get("moneyline", {})
        if ml:
            home_ml = ml.get("home", {})
            away_ml = ml.get("away", {})
            moneyline = Moneyline(
                home_team=home_team,
                away_team=away_team,
                home_odds=home_ml.get("close", 0) if home_ml else 0,
                away_odds=away_ml.get("close", 0) if away_ml else 0,
                provider=provider,
            )

        total = None
        if "overUnder" in odds_data:
            ou = odds_data.get("overUnder", 0)
            total_data = odds_data.get("total", {})
            total = Total(
                over_under=float(ou) if ou else 0,
                over_odds=total_data.get("over", {}).get("close", 0) if total_data else 0,
                under_odds=total_data.get("under", {}).get("close", 0) if total_data else 0,
                provider=provider,
            )

        return GameOdds(
            event_id=event.get("id", ""),
            home_team=home_team,
            away_team=away_team,
            spread=spread,
            moneyline=moneyline,
            total=total,
        )

    @staticmethod
    def from_scoreboard(scoreboard: dict[str, Any]) -> list[GameOdds]:
        """Extract all odds from a scoreboard response.

        Args:
            scoreboard: Full scoreboard API response.

        Returns:
            List of GameOdds objects.
        """
        results = []
        events = scoreboard.get("events", [])
        for event in events:
            odds = Odds.from_event(event)
            if odds:
                results.append(odds)
        return results

    @staticmethod
    def spreads(scoreboard: dict[str, Any]) -> list[dict[str, Any]]:
        """Get all spreads from scoreboard as simple dicts.

        Args:
            scoreboard: Full scoreboard API response.

        Returns:
            List of spread dicts with game info.
        """
        results = []
        for odds in Odds.from_scoreboard(scoreboard):
            if odds.spread:
                results.append(
                    {
                        "event_id": odds.event_id,
                        "home": odds.home_team,
                        "away": odds.away_team,
                        "favorite": odds.spread.favorite,
                        "spread": odds.spread.spread,
                        "provider": odds.spread.provider,
                    }
                )
        return results

    @staticmethod
    def moneylines(scoreboard: dict[str, Any]) -> list[dict[str, Any]]:
        """Get all moneylines from scoreboard as simple dicts.

        Args:
            scoreboard: Full scoreboard API response.

        Returns:
            List of moneyline dicts with game info.
        """
        results = []
        for odds in Odds.from_scoreboard(scoreboard):
            if odds.moneyline:
                results.append(
                    {
                        "event_id": odds.event_id,
                        "home": odds.home_team,
                        "away": odds.away_team,
                        "home_odds": odds.moneyline.home_odds,
                        "away_odds": odds.moneyline.away_odds,
                        "provider": odds.moneyline.provider,
                    }
                )
        return results

    @staticmethod
    def totals(scoreboard: dict[str, Any]) -> list[dict[str, Any]]:
        """Get all over/unders from scoreboard as simple dicts.

        Args:
            scoreboard: Full scoreboard API response.

        Returns:
            List of total dicts with game info.
        """
        results = []
        for odds in Odds.from_scoreboard(scoreboard):
            if odds.total:
                results.append(
                    {
                        "event_id": odds.event_id,
                        "home": odds.home_team,
                        "away": odds.away_team,
                        "over_under": odds.total.over_under,
                        "over_odds": odds.total.over_odds,
                        "under_odds": odds.total.under_odds,
                        "provider": odds.total.provider,
                    }
                )
        return results
