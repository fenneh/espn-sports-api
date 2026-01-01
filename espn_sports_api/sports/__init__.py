"""Sport-specific API modules."""

from .nfl import NFL
from .nba import NBA
from .mlb import MLB
from .nhl import NHL
from .soccer import Soccer
from .ufc import UFC
from .golf import Golf
from .racing import Racing
from .tennis import Tennis
from .college import NCAAF, NCAAB, WomensNCAAB, CollegeBaseball
from .wnba import WNBA

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
]
