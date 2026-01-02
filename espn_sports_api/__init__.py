"""ESPN Sports API - Python client for ESPN's public API."""

from typing import Any

from .client import Cache, ESPNClient
from .constants import (
    Conferences,
    MLBDivision,
    NBAConference,
    NCAABConference,
    NCAAFConference,
    NFLDivision,
)
from .fantasy import (
    FantasyBaseball,
    FantasyBasketball,
    FantasyFootball,
    FantasyHockey,
    FantasyLeague,
)
from .models import (
    Athlete,
    Broadcast,
    Injury,
    Team,
    Transaction,
    Venue,
    Weather,
    parse_athletes,
    parse_injuries,
    parse_teams,
    parse_transactions,
    parse_venues,
)
from .odds import GameOdds, Moneyline, Odds, Spread, Total
from .sports import (
    CFL,
    MLB,
    NBA,
    NCAAB,
    NCAAF,
    NFL,
    NHL,
    UFC,
    WNBA,
    XFL,
    CollegeBaseball,
    Golf,
    Racing,
    Soccer,
    Tennis,
    WomensNCAAB,
)


def quick_scores(sport: str = "nfl") -> dict[str, Any]:
    """Get today's scores for a sport in one line.

    Args:
        sport: Sport name. Options: nfl, nba, mlb, nhl, ncaaf, ncaab, wnba, mls.

    Returns:
        Scoreboard data for today.

    Example:
        >>> from espn_sports_api import quick_scores
        >>> scores = quick_scores("nba")
        >>> for event in scores.get("events", []):
        ...     print(event["name"])
    """
    sport_map = {
        "nfl": NFL,
        "nba": NBA,
        "mlb": MLB,
        "nhl": NHL,
        "ncaaf": NCAAF,
        "ncaab": NCAAB,
        "wnba": WNBA,
        "mls": lambda: Soccer(league="mls"),
        "epl": lambda: Soccer(league="epl"),
    }
    cls = sport_map.get(sport.lower())
    if cls is None:
        raise ValueError(f"Unknown sport: {sport}. Options: {', '.join(sport_map.keys())}")
    instance = cls() if callable(cls) else cls()
    return instance.today()


__version__ = "0.3.1"
__all__ = [
    # Client
    "ESPNClient",
    "Cache",
    # Sports
    "NFL",
    "NBA",
    "MLB",
    "NHL",
    "Soccer",
    "UFC",
    "Golf",
    "Racing",
    "Tennis",
    "NCAAF",
    "NCAAB",
    "WomensNCAAB",
    "CollegeBaseball",
    "WNBA",
    "CFL",
    "XFL",
    # Fantasy
    "FantasyFootball",
    "FantasyBasketball",
    "FantasyBaseball",
    "FantasyHockey",
    "FantasyLeague",
    # Odds
    "Odds",
    "GameOdds",
    "Spread",
    "Moneyline",
    "Total",
    # Models
    "Venue",
    "Broadcast",
    "Weather",
    "Injury",
    "Transaction",
    "Athlete",
    "Team",
    "parse_injuries",
    "parse_transactions",
    "parse_venues",
    "parse_athletes",
    "parse_teams",
    # Constants
    "Conferences",
    "NCAAFConference",
    "NCAABConference",
    "NFLDivision",
    "NBAConference",
    "MLBDivision",
    # Utilities
    "quick_scores",
]
