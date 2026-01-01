"""Soccer API module."""

from __future__ import annotations

from typing import Any, Optional

from .base import BaseSport


class Soccer(BaseSport):
    """Soccer/Football API access."""

    SPORT = "soccer"
    LEAGUE = "eng.1"  # Default to Premier League

    # Common league codes
    LEAGUES = {
        # England
        "epl": "eng.1",
        "premier_league": "eng.1",
        "championship": "eng.2",
        "league_one": "eng.3",
        "league_two": "eng.4",
        "fa_cup": "eng.fa",
        "efl_cup": "eng.league_cup",
        "community_shield": "eng.charity",
        # Spain
        "la_liga": "esp.1",
        "segunda": "esp.2",
        "copa_del_rey": "esp.copa_del_rey",
        "supercopa": "esp.super_cup",
        # Germany
        "bundesliga": "ger.1",
        "2_bundesliga": "ger.2",
        "dfb_pokal": "ger.dfb_pokal",
        "super_cup": "ger.super_cup",
        # Italy
        "serie_a": "ita.1",
        "serie_b": "ita.2",
        "coppa_italia": "ita.coppa_italia",
        "supercoppa": "ita.super_cup",
        # France
        "ligue_1": "fra.1",
        "ligue_2": "fra.2",
        "coupe_de_france": "fra.coupe_de_france",
        "trophee_champions": "fra.super_cup",
        # Americas
        "mls": "usa.1",
        "nwsl": "usa.nwsl",
        "usl_championship": "usa.usl.1",
        "us_open_cup": "usa.open",
        "liga_mx": "mex.1",
        "liga_mx_w": "mex.w.1",
        "copa_mx": "mex.copa_mx",
        "brazilian_serie_a": "bra.1",
        "brazilian_serie_b": "bra.2",
        "copa_do_brasil": "bra.copa_do_brasil",
        "argentina_primera": "arg.1",
        "copa_argentina": "arg.copa",
        # UEFA Competitions
        "champions_league": "uefa.champions",
        "europa_league": "uefa.europa",
        "conference_league": "uefa.europa.conf",
        "uefa_super_cup": "uefa.super_cup",
        "euro": "uefa.euro",
        "euro_qualifiers": "uefa.euroq",
        "nations_league": "uefa.nations",
        # FIFA/International
        "world_cup": "fifa.world",
        "world_cup_qualifiers": "fifa.worldq",
        "world_cup_women": "fifa.wwc",
        "club_world_cup": "fifa.cwc",
        "olympics_men": "fifa.olympics",
        "olympics_women": "fifa.w.olympics",
        "friendly": "fifa.friendly",
        # CONMEBOL
        "copa_libertadores": "conmebol.libertadores",
        "copa_sudamericana": "conmebol.sudamericana",
        "copa_america": "conmebol.america",
        # CONCACAF
        "concacaf_champions": "concacaf.champions",
        "concacaf_gold_cup": "concacaf.gold",
        "concacaf_nations": "concacaf.nations.league",
        # Other Europe
        "eredivisie": "ned.1",
        "eerste_divisie": "ned.2",
        "knvb_cup": "ned.cup",
        "primeira_liga": "por.1",
        "taca_portugal": "por.cup",
        "scottish_premiership": "sco.1",
        "scottish_cup": "sco.cup",
        "belgian_pro_league": "bel.1",
        "super_lig": "tur.1",
        "turkish_cup": "tur.cup",
        "swiss_super_league": "sui.1",
        "austrian_bundesliga": "aut.1",
        "greek_super_league": "gre.1",
        "russian_premier": "rus.1",
        "ukrainian_premier": "ukr.1",
        "danish_superliga": "den.1",
        "norwegian_eliteserien": "nor.1",
        "swedish_allsvenskan": "swe.1",
        "polish_ekstraklasa": "pol.1",
        "czech_liga": "cze.1",
        "croatian_hnl": "cro.1",
        "serbian_superliga": "srb.1",
        # Asia
        "afc_champions": "afc.champions",
        "asian_cup": "afc.cup",
        "j_league": "jpn.1",
        "k_league": "kor.1",
        "csl": "chn.1",
        "a_league": "aus.1",
        "saudi_pro_league": "sau.1",
        "indian_super_league": "ind.1",
        # Africa
        "caf_champions": "caf.champions",
        "afcon": "caf.nations",
        "egyptian_premier": "egy.1",
        "south_african_psl": "rsa.1",
    }

    def __init__(self, league: str = "epl", client=None):
        """Initialize soccer module.

        Args:
            league: League code (e.g., 'epl', 'la_liga') or ESPN code (e.g., 'eng.1').
            client: ESPN client instance.
        """
        super().__init__(client)
        self.LEAGUE = self.LEAGUES.get(league.lower(), league)

    def team_schedule(
        self,
        team_id: str,
        season: Optional[int] = None,
        fixtures: bool = False,
    ) -> dict[str, Any]:
        """Get team schedule.

        Args:
            team_id: Team ID.
            season: Season year.
            fixtures: If True, get upcoming fixtures. If False, get results.

        Returns:
            Schedule data.
        """
        params = {}
        if season:
            params["season"] = season
        if fixtures:
            params["fixture"] = "true"
        # Soccer uses 'all' league for team schedules
        return self.client.get(f"soccer/all/teams/{team_id}/schedule", params or None)

    @staticmethod
    def all_leagues_scoreboard(dates: Optional[str] = None) -> dict[str, Any]:
        """Get scoreboard across all leagues.

        Args:
            dates: Date filter (YYYYMMDD format).

        Returns:
            Scoreboard data from all leagues.
        """
        from ..client import ESPNClient

        client = ESPNClient()
        params = {"dates": dates} if dates else None
        return client.get("soccer/all/scoreboard", params)

    def table(self) -> dict[str, Any]:
        """Get league table/standings.

        Returns:
            League table data.
        """
        return self.standings()

    def transfers(self) -> dict[str, Any]:
        """Get transfer news.

        Returns:
            Transfer data.
        """
        return self.client.get_core(f"{self._core_endpoint()}/transfers")

    @classmethod
    def available_leagues(cls) -> dict[str, str]:
        """Get available league codes.

        Returns:
            Dictionary of friendly names to ESPN codes.
        """
        return cls.LEAGUES.copy()
