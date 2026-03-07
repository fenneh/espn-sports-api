"""Integration smoke tests that hit the real ESPN API.

These verify ESPN endpoints are alive and returning expected shapes.
Run with: pytest -m integration
"""

import pytest

from espn_sports_api import (
    MLB,
    NBA,
    NCAAB,
    NCAAF,
    NFL,
    NHL,
    UFC,
    ESPNClient,
    Golf,
    Racing,
    Soccer,
    Tennis,
    quick_scores,
)

pytestmark = pytest.mark.integration


class TestClientSmoke:
    def test_get_nfl_scoreboard(self):
        client = ESPNClient()
        response = client.get("football/nfl/scoreboard")
        assert "events" in response or "leagues" in response

    def test_get_nfl_teams(self):
        client = ESPNClient()
        response = client.get("football/nfl/teams")
        assert "sports" in response

    def test_get_core_athletes(self):
        client = ESPNClient()
        response = client.get_core("football/leagues/nfl/athletes?limit=5")
        assert "items" in response or "count" in response

    def test_invalid_endpoint_raises(self):
        client = ESPNClient()
        with pytest.raises(Exception):
            client.get("invalid/endpoint/that/does/not/exist")


class TestNFLSmoke:
    def test_scoreboard(self):
        assert isinstance(NFL().scoreboard(), dict)

    def test_scoreboard_with_dates(self):
        assert isinstance(NFL().scoreboard(dates="20241201"), dict)

    def test_teams(self):
        assert "sports" in NFL().teams()

    def test_team(self):
        assert "team" in NFL().team("ne")

    def test_news(self):
        response = NFL().news(limit=5)
        assert "articles" in response or "header" in response

    def test_standings(self):
        assert isinstance(NFL().standings(), dict)

    def test_injuries(self):
        assert isinstance(NFL().injuries(), dict)

    def test_statistics(self):
        assert isinstance(NFL().statistics(), dict)


class TestNBASmoke:
    def test_scoreboard(self):
        assert isinstance(NBA().scoreboard(), dict)

    def test_teams(self):
        assert "sports" in NBA().teams()

    def test_team(self):
        assert "team" in NBA().team("lal")


class TestMLBSmoke:
    def test_scoreboard(self):
        assert isinstance(MLB().scoreboard(), dict)

    def test_teams(self):
        assert "sports" in MLB().teams()


class TestNHLSmoke:
    def test_scoreboard(self):
        assert isinstance(NHL().scoreboard(), dict)

    def test_teams(self):
        assert "sports" in NHL().teams()


class TestSoccerSmoke:
    def test_scoreboard(self):
        assert isinstance(Soccer(league="epl").scoreboard(), dict)

    def test_teams(self):
        assert "sports" in Soccer(league="epl").teams()

    def test_table(self):
        assert isinstance(Soccer(league="epl").table(), dict)


class TestUFCSmoke:
    def test_scoreboard(self):
        assert isinstance(UFC().scoreboard(), dict)


class TestGolfSmoke:
    def test_scoreboard(self):
        assert isinstance(Golf().scoreboard(), dict)


class TestRacingSmoke:
    def test_scoreboard(self):
        assert isinstance(Racing(series="f1").scoreboard(), dict)


class TestTennisSmoke:
    def test_scoreboard(self):
        assert isinstance(Tennis().scoreboard(), dict)


class TestNCAAFSmoke:
    def test_scoreboard(self):
        assert isinstance(NCAAF().scoreboard(), dict)

    def test_rankings(self):
        assert isinstance(NCAAF().rankings(), dict)


class TestNCAABSmoke:
    def test_scoreboard(self):
        assert isinstance(NCAAB().scoreboard(), dict)


class TestConvenienceSmoke:
    def test_today(self):
        assert isinstance(NFL().today(), dict)

    def test_yesterday(self):
        assert isinstance(NFL().yesterday(), dict)

    def test_tomorrow(self):
        assert isinstance(NFL().tomorrow(), dict)

    def test_on_date(self):
        from datetime import date

        assert isinstance(NFL().on_date(date(2024, 12, 1)), dict)

    def test_date_range(self):
        from datetime import date

        assert isinstance(NFL().date_range(date(2024, 12, 1), date(2024, 12, 7)), dict)

    def test_live(self):
        response = NFL().live()
        assert isinstance(response, dict)
        assert "events" in response

    def test_for_week(self):
        assert isinstance(NFL().for_week(1), dict)

    def test_athletes(self):
        assert isinstance(NFL().athletes(limit=5), dict)

    def test_seasons(self):
        assert isinstance(NFL().seasons(2024), dict)

    def test_context_manager(self):
        with NFL() as sport:
            assert "sports" in sport.teams()

    def test_quick_scores_nfl(self):
        assert isinstance(quick_scores("nfl"), dict)

    def test_quick_scores_nba(self):
        assert isinstance(quick_scores("nba"), dict)

    def test_quick_scores_mls(self):
        assert isinstance(quick_scores("mls"), dict)


class TestCollegeConferenceSmoke:
    def test_ncaaf_with_conference_string(self):
        assert isinstance(NCAAF().scoreboard(conference="SEC"), dict)

    def test_ncaab_with_conference_string(self):
        assert isinstance(NCAAB().scoreboard(conference="BIG_EAST"), dict)
