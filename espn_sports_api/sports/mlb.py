"""MLB API module."""

from __future__ import annotations

from .base import DraftTransactionsMixin


class MLB(DraftTransactionsMixin):
    """MLB-specific API access."""

    SPORT = "baseball"
    LEAGUE = "mlb"
