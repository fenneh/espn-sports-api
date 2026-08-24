"""NHL API module."""

from __future__ import annotations

from .base import DraftTransactionsMixin


class NHL(DraftTransactionsMixin):
    """NHL-specific API access."""

    SPORT = "hockey"
    LEAGUE = "nhl"
