"""CFL (Canadian Football League) API module."""

from typing import Any

from .base import BaseSport


class CFL(BaseSport):
    """Canadian Football League API access."""

    SPORT = "football"
    LEAGUE = "cfl"

    def grey_cup(self) -> dict[str, Any]:
        """Get Grey Cup championship information.

        Returns:
            Grey Cup data.
        """
        return self.client.get(f"{self._endpoint()}/rankings")
