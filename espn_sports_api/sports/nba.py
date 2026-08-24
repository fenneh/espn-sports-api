"""NBA API module."""

from __future__ import annotations

from .base import DraftTransactionsMixin


class NBA(DraftTransactionsMixin):
    """NBA-specific API access."""

    SPORT = "basketball"
    LEAGUE = "nba"
