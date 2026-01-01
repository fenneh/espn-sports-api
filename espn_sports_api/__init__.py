"""ESPN Sports API - Python client for ESPN's public API."""

from .client import Cache, ESPNClient
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

__version__ = "0.2.0"
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
]
