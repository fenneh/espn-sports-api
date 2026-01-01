"""XFL API module."""

from __future__ import annotations

from .base import BaseSport


class XFL(BaseSport):
    """XFL API access."""

    SPORT = "football"
    LEAGUE = "xfl"
