"""Sport-specific API modules."""

from .cfl import CFL
from .college import NCAAB, NCAAF, CollegeBaseball, WomensNCAAB
from .golf import Golf
from .mlb import MLB
from .nba import NBA
from .nfl import NFL
from .nhl import NHL
from .racing import Racing
from .soccer import Soccer
from .tennis import Tennis
from .ufc import UFC
from .wnba import WNBA
from .xfl import XFL

__all__ = [
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
]
