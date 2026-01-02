"""Constants for ESPN API including conference and group IDs."""

from __future__ import annotations

from enum import IntEnum
from typing import Optional


class NCAAFConference(IntEnum):
    """NCAA Football conference group IDs for filtering scoreboards."""

    FBS = 80
    FCS = 81
    SEC = 8
    BIG_TEN = 5
    BIG_12 = 4
    ACC = 1
    PAC_12 = 9
    AAC = 151
    MOUNTAIN_WEST = 17
    SUN_BELT = 37
    MAC = 15
    CUSA = 12
    INDEPENDENT = 18
    IVY = 22


class NCAABConference(IntEnum):
    """NCAA Men's Basketball conference group IDs."""

    SEC = 3
    BIG_TEN = 7
    BIG_12 = 8
    ACC = 2
    PAC_12 = 21
    BIG_EAST = 4
    AAC = 62
    MOUNTAIN_WEST = 44
    ATLANTIC_10 = 3
    WCC = 26
    MVC = 18
    IVY = 22
    SOUTHERN = 24
    COLONIAL = 10
    HORIZON = 48
    MAAC = 45


class NFLDivision(IntEnum):
    """NFL conference and division IDs."""

    AFC = 1
    NFC = 2
    AFC_EAST = 4
    AFC_NORTH = 12
    AFC_SOUTH = 13
    AFC_WEST = 6
    NFC_EAST = 1
    NFC_NORTH = 10
    NFC_SOUTH = 8
    NFC_WEST = 7


class NBAConference(IntEnum):
    """NBA conference and division IDs."""

    EASTERN = 5
    WESTERN = 6
    ATLANTIC = 1
    CENTRAL = 2
    SOUTHEAST = 3
    NORTHWEST = 4
    PACIFIC = 7
    SOUTHWEST = 8


class MLBDivision(IntEnum):
    """MLB league and division IDs."""

    AMERICAN = 1
    NATIONAL = 2
    AL_EAST = 3
    AL_CENTRAL = 4
    AL_WEST = 5
    NL_EAST = 6
    NL_CENTRAL = 7
    NL_WEST = 8


class Conferences:
    """Lookup utilities for conference/division IDs.

    Example:
        >>> from espn_sports_api import Conferences, NCAAFConference
        >>> Conferences.get("ncaaf", "SEC")
        8
        >>> NCAAFConference.SEC
        <NCAAFConference.SEC: 8>
    """

    NCAAF = NCAAFConference
    NCAAB = NCAABConference
    NFL = NFLDivision
    NBA = NBAConference
    MLB = MLBDivision

    @classmethod
    def get(cls, sport: str, name: str) -> Optional[int]:
        """Look up a conference/division ID by name.

        Args:
            sport: Sport name ('ncaaf', 'ncaab', 'nfl', 'nba', 'mlb').
            name: Conference/division name (case-insensitive, underscores optional).

        Returns:
            Conference ID or None if not found.

        Example:
            >>> Conferences.get("ncaaf", "SEC")
            8
            >>> Conferences.get("nfl", "AFC East")
            4
            >>> Conferences.get("ncaab", "big ten")
            7
        """
        mapping = {
            "ncaaf": cls.NCAAF,
            "ncaab": cls.NCAAB,
            "nfl": cls.NFL,
            "nba": cls.NBA,
            "mlb": cls.MLB,
        }
        enum_class = mapping.get(sport.lower())
        if not enum_class:
            return None

        normalized = name.upper().replace(" ", "_").replace("-", "_")
        try:
            return enum_class[normalized].value
        except KeyError:
            return None

    @classmethod
    def list_all(cls, sport: str) -> dict[str, int]:
        """List all conferences/divisions for a sport.

        Args:
            sport: Sport name.

        Returns:
            Dictionary of name to ID mappings.

        Example:
            >>> Conferences.list_all("ncaaf")
            {'FBS': 80, 'FCS': 81, 'SEC': 8, ...}
        """
        mapping = {
            "ncaaf": cls.NCAAF,
            "ncaab": cls.NCAAB,
            "nfl": cls.NFL,
            "nba": cls.NBA,
            "mlb": cls.MLB,
        }
        enum_class = mapping.get(sport.lower())
        if not enum_class:
            return {}
        return {member.name: member.value for member in enum_class}
