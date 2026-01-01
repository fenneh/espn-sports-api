"""ESPN Sports API - Python client for ESPN's public API."""

from .client import ESPNClient
from .fantasy import (
    FantasyFootball,
    FantasyBasketball,
    FantasyBaseball,
    FantasyHockey,
    FantasyLeague,
)
from .odds import Odds, GameOdds, Spread, Moneyline, Total
from .models import (
    Venue,
    Broadcast,
    Weather,
    Injury,
    Transaction,
    Athlete,
    Team,
    parse_injuries,
    parse_transactions,
    parse_venues,
    parse_athletes,
    parse_teams,
)
from .sports import (
    NFL,
    NBA,
    MLB,
    NHL,
    Soccer,
    UFC,
    Golf,
    Racing,
    Tennis,
    NCAAF,
    NCAAB,
    WomensNCAAB,
    CollegeBaseball,
    WNBA,
    CFL,
    XFL,
)

__version__ = "0.2.0"
__all__ = [
    # Client
    "ESPNClient",
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
