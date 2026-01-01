"""ESPN Sports API - Python client for ESPN's public API."""

from .client import ESPNClient
from .fantasy import (
    FantasyFootball,
    FantasyBasketball,
    FantasyBaseball,
    FantasyHockey,
    FantasyLeague,
)
from .sports import NFL, NBA, MLB, NHL, Soccer, UFC, Golf, Racing, Tennis, NCAAF, NCAAB, WNBA

__version__ = "0.1.0"
__all__ = [
    "ESPNClient",
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
    "WNBA",
    "FantasyFootball",
    "FantasyBasketball",
    "FantasyBaseball",
    "FantasyHockey",
    "FantasyLeague",
]
