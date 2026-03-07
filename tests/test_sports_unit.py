"""Unit tests for sport modules with mocked HTTP responses."""

from unittest.mock import patch

import responses

from espn_sports_api import CFL, NCAAB, NCAAF, NFL, XFL, SeasonType, Soccer
from espn_sports_api.constants import NCAABConference, NCAAFConference
from espn_sports_api.sports.college import _resolve_conference

BASE = "https://site.api.espn.com/apis/site/v2/sports"
CORE = "https://sports.core.api.espn.com/v2/sports"
STANDINGS = "https://site.api.espn.com/apis/v2/sports"
WEB = "https://site.web.api.espn.com/apis/common/v3/sports"


class TestBaseSportMethods:
    """Test BaseSport methods via NFL."""

    @responses.activate
    def test_scoreboard_all_params(self):
        responses.add(responses.GET, f"{BASE}/football/nfl/scoreboard", json={"events": []})
        nfl = NFL()
        nfl.scoreboard(
            dates="20241201",
            limit=10,
            groups=5,
            calendar=True,
            season=2024,
            seasontype=2,
            week=10,
        )
        url = responses.calls[0].request.url
        assert "dates=20241201" in url
        assert "limit=10" in url
        assert "groups=5" in url
        assert "calendar=true" in url
        assert "season=2024" in url
        assert "seasontype=2" in url
        assert "week=10" in url

    @responses.activate
    def test_news_passes_limit_param(self):
        responses.add(
            responses.GET, f"{BASE}/football/nfl/news", json={"articles": [{"headline": "X"}]}
        )
        data = NFL().news(limit=5)
        assert data["articles"][0]["headline"] == "X"
        assert "limit=5" in responses.calls[0].request.url

    @responses.activate
    def test_news_without_limit_omits_param(self):
        responses.add(responses.GET, f"{BASE}/football/nfl/news", json={"articles": []})
        data = NFL().news()
        assert data == {"articles": []}
        assert "limit" not in (responses.calls[0].request.url or "")

    @responses.activate
    def test_teams(self):
        responses.add(responses.GET, f"{BASE}/football/nfl/teams", json={"sports": []})
        data = NFL().teams()
        assert "sports" in data

    @responses.activate
    def test_team(self):
        responses.add(responses.GET, f"{BASE}/football/nfl/teams/ne", json={"team": {}})
        data = NFL().team("ne")
        assert "team" in data

    @responses.activate
    def test_standings_with_params(self):
        responses.add(responses.GET, f"{BASE}/football/nfl/standings", json={"standings": []})
        NFL().standings(season=2024, group="conference")
        url = responses.calls[0].request.url
        assert "season=2024" in url
        assert "group=conference" in url

    @responses.activate
    def test_standings_no_params_omits_query_string(self):
        responses.add(
            responses.GET, f"{BASE}/football/nfl/standings", json={"children": [{"name": "AFC"}]}
        )
        data = NFL().standings()
        assert data["children"][0]["name"] == "AFC"
        assert "?" not in (responses.calls[0].request.url or "")

    @responses.activate
    def test_athletes_with_limit(self):
        responses.add(responses.GET, f"{CORE}/football/leagues/nfl/athletes", json={"items": []})
        NFL().athletes(limit=10)
        assert "limit=10" in responses.calls[0].request.url

    @responses.activate
    def test_base_injuries_returns_mock_data(self):
        mock = {"injuries": [{"name": "Player X"}]}
        responses.add(responses.GET, f"{BASE}/football/nfl/injuries", json=mock)
        assert NFL().injuries() == mock

    @responses.activate
    def test_today_passes_todays_date(self):
        from datetime import date

        responses.add(
            responses.GET, f"{BASE}/football/nfl/scoreboard", json={"events": [{"id": "1"}]}
        )
        data = NFL().today()
        assert data["events"][0]["id"] == "1"
        expected_date = date.today().strftime("%Y%m%d")
        assert f"dates={expected_date}" in responses.calls[0].request.url

    @responses.activate
    def test_yesterday_passes_yesterdays_date(self):
        from datetime import date, timedelta

        responses.add(responses.GET, f"{BASE}/football/nfl/scoreboard", json={"events": []})
        NFL().yesterday()
        expected = (date.today() - timedelta(days=1)).strftime("%Y%m%d")
        assert f"dates={expected}" in responses.calls[0].request.url

    @responses.activate
    def test_tomorrow_passes_tomorrows_date(self):
        from datetime import date, timedelta

        responses.add(responses.GET, f"{BASE}/football/nfl/scoreboard", json={"events": []})
        NFL().tomorrow()
        expected = (date.today() + timedelta(days=1)).strftime("%Y%m%d")
        assert f"dates={expected}" in responses.calls[0].request.url

    @responses.activate
    def test_on_date_with_date_obj(self):
        from datetime import date

        responses.add(responses.GET, f"{BASE}/football/nfl/scoreboard", json={"events": []})
        NFL().on_date(date(2024, 12, 1))
        assert "dates=20241201" in responses.calls[0].request.url

    @responses.activate
    def test_on_date_with_string(self):
        responses.add(responses.GET, f"{BASE}/football/nfl/scoreboard", json={"events": []})
        NFL().on_date("20241225")
        assert "dates=20241225" in responses.calls[0].request.url

    @responses.activate
    def test_date_range(self):
        from datetime import date

        responses.add(responses.GET, f"{BASE}/football/nfl/scoreboard", json={"events": []})
        NFL().date_range(date(2024, 12, 1), date(2024, 12, 7))
        assert "dates=20241201-20241207" in responses.calls[0].request.url

    @responses.activate
    def test_date_range_strings(self):
        responses.add(responses.GET, f"{BASE}/football/nfl/scoreboard", json={"events": []})
        NFL().date_range("20241201", "20241207")
        assert "dates=20241201-20241207" in responses.calls[0].request.url

    @responses.activate
    def test_live_filters_in_progress(self):
        responses.add(
            responses.GET,
            f"{BASE}/football/nfl/scoreboard",
            json={
                "events": [
                    {"name": "live", "status": {"type": {"state": "in"}}},
                    {"name": "final", "status": {"type": {"state": "post"}}},
                ]
            },
        )
        data = NFL().live()
        assert len(data["events"]) == 1
        assert data["events"][0]["name"] == "live"

    @responses.activate
    def test_for_week(self):
        responses.add(responses.GET, f"{BASE}/football/nfl/scoreboard", json={"events": []})
        NFL().for_week(10, season=2024)
        url = responses.calls[0].request.url
        assert "week=10" in url
        assert "season=2024" in url

    def test_close_owned_client(self):
        nfl = NFL()
        assert nfl._owns_client is True
        with patch.object(nfl.client, "close") as mock_close:
            nfl.close()
            mock_close.assert_called_once()

    def test_close_external_client_noop(self):
        from espn_sports_api import ESPNClient

        client = ESPNClient()
        nfl = NFL(client=client)
        assert nfl._owns_client is False
        with patch.object(nfl.client, "close") as mock_close:
            nfl.close()
            mock_close.assert_not_called()

    def test_context_manager(self):
        with patch.object(NFL, "close") as mock_close:
            with NFL() as nfl:
                assert nfl is not None
            mock_close.assert_called_once()

    @responses.activate
    def test_team_roster(self):
        responses.add(
            responses.GET,
            f"{BASE}/football/nfl/teams/ne/roster",
            json={"athletes": []},
        )
        nfl = NFL()
        data = nfl.team_roster("ne")
        assert "athletes" in data

    @responses.activate
    def test_team_schedule(self):
        responses.add(
            responses.GET,
            f"{BASE}/football/nfl/teams/ne/schedule",
            json={"events": []},
        )
        nfl = NFL()
        data = nfl.team_schedule("ne")
        assert "events" in data

    @responses.activate
    def test_team_schedule_with_season(self):
        responses.add(
            responses.GET,
            f"{BASE}/football/nfl/teams/ne/schedule",
            json={"events": []},
        )
        nfl = NFL()
        nfl.team_schedule("ne", season=2024)
        assert "season=2024" in responses.calls[0].request.url

    @responses.activate
    def test_event(self):
        responses.add(
            responses.GET,
            f"{BASE}/football/nfl/summary",
            json={"header": {}, "boxscore": {}},
        )
        nfl = NFL()
        nfl.event("401547417")
        assert "event=401547417" in responses.calls[0].request.url

    @responses.activate
    def test_playbyplay_returns_summary_data(self):
        mock = {"drives": [{"description": "TD drive"}]}
        responses.add(responses.GET, f"{BASE}/football/nfl/summary", json=mock)
        data = NFL().playbyplay("401547417")
        assert data == mock
        assert "event=401547417" in responses.calls[0].request.url

    @responses.activate
    def test_box_score_returns_summary_data(self):
        mock = {"boxscore": {"teams": []}}
        responses.add(responses.GET, f"{BASE}/football/nfl/summary", json=mock)
        data = NFL().box_score("401547417")
        assert data == mock

    @responses.activate
    def test_athlete(self):
        responses.add(
            responses.GET,
            f"{CORE}/football/leagues/nfl/athletes/12345",
            json={"id": "12345", "displayName": "Test Player"},
        )
        nfl = NFL()
        data = nfl.athlete("12345")
        assert data["id"] == "12345"

    @responses.activate
    def test_athlete_stats(self):
        responses.add(
            responses.GET,
            f"{WEB}/football/leagues/nfl/athletes/12345/stats",
            json={"statistics": []},
        )
        nfl = NFL()
        data = nfl.athlete_stats("12345")
        assert "statistics" in data

    @responses.activate
    def test_team_injuries(self):
        responses.add(
            responses.GET,
            f"{CORE}/football/leagues/nfl/teams/ne/injuries",
            json={"items": []},
        )
        nfl = NFL()
        data = nfl.team_injuries("ne")
        assert "items" in data

    @responses.activate
    def test_transactions_returns_mock_data(self):
        mock = {"transactions": [{"type": "trade"}]}
        responses.add(responses.GET, f"{BASE}/football/nfl/transactions", json=mock)
        assert NFL().transactions() == mock

    @responses.activate
    def test_statistics_without_category(self):
        mock = {"categories": [{"name": "passing"}]}
        responses.add(responses.GET, f"{BASE}/football/nfl/statistics", json=mock)
        assert NFL().statistics() == mock

    @responses.activate
    def test_statistics_appends_category_to_path(self):
        mock = {"leaders": [{"name": "Mahomes"}]}
        responses.add(responses.GET, f"{BASE}/football/nfl/statistics/passing", json=mock)
        assert NFL().statistics(category="passing") == mock

    @responses.activate
    def test_venues(self):
        responses.add(
            responses.GET,
            f"{CORE}/football/leagues/nfl/venues",
            json={"items": []},
        )
        nfl = NFL()
        data = nfl.venues()
        assert "items" in data

    @responses.activate
    def test_franchises(self):
        responses.add(
            responses.GET,
            f"{CORE}/football/leagues/nfl/franchises",
            json={"items": []},
        )
        nfl = NFL()
        data = nfl.franchises()
        assert data == {"items": []}

    @responses.activate
    def test_events(self):
        responses.add(
            responses.GET,
            f"{CORE}/football/leagues/nfl/events",
            json={"items": []},
        )
        nfl = NFL()
        data = nfl.events()
        assert data == {"items": []}

    @responses.activate
    def test_events_with_params(self):
        responses.add(
            responses.GET,
            f"{CORE}/football/leagues/nfl/events",
            json={"items": []},
        )
        nfl = NFL()
        nfl.events(dates="20241201", limit=10)
        assert "dates=20241201" in responses.calls[0].request.url
        assert "limit=10" in responses.calls[0].request.url

    @responses.activate
    def test_positions(self):
        responses.add(
            responses.GET,
            f"{CORE}/football/leagues/nfl/positions",
            json={"items": []},
        )
        nfl = NFL()
        data = nfl.positions()
        assert data == {"items": []}

    @responses.activate
    def test_leaders(self):
        responses.add(
            responses.GET,
            f"{CORE}/football/leagues/nfl/leaders",
            json={"categories": []},
        )
        nfl = NFL()
        data = nfl.leaders()
        assert data == {"categories": []}

    @responses.activate
    def test_leaders_with_category(self):
        responses.add(
            responses.GET,
            f"{CORE}/football/leagues/nfl/leaders/passing",
            json={"leaders": []},
        )
        nfl = NFL()
        data = nfl.leaders(category="passing")
        assert data == {"leaders": []}

    @responses.activate
    def test_seasons(self):
        responses.add(
            responses.GET,
            f"{CORE}/football/leagues/nfl/seasons/2024",
            json={"year": 2024},
        )
        nfl = NFL()
        data = nfl.seasons(year=2024)
        assert data["year"] == 2024

    @responses.activate
    def test_seasons_no_year(self):
        responses.add(
            responses.GET,
            f"{CORE}/football/leagues/nfl/seasons",
            json={"items": []},
        )
        nfl = NFL()
        data = nfl.seasons()
        assert data == {"items": []}


class TestSeasonTypeEnum:
    """Test SeasonType enum usage."""

    @responses.activate
    def test_scoreboard_with_season_type_enum(self):
        responses.add(
            responses.GET,
            f"{BASE}/football/nfl/scoreboard",
            json={"events": []},
        )
        nfl = NFL()
        nfl.scoreboard(seasontype=SeasonType.POSTSEASON)
        assert "seasontype=3" in responses.calls[0].request.url

    @responses.activate
    def test_scoreboard_with_season_type_int(self):
        responses.add(
            responses.GET,
            f"{BASE}/football/nfl/scoreboard",
            json={"events": []},
        )
        nfl = NFL()
        nfl.scoreboard(seasontype=2)
        assert "seasontype=2" in responses.calls[0].request.url

    def test_season_type_values(self):
        assert SeasonType.PRESEASON == 1
        assert SeasonType.REGULAR == 2
        assert SeasonType.POSTSEASON == 3
        assert SeasonType.OFFSEASON == 4


class TestSoccerUnit:
    """Unit tests for Soccer module."""

    @responses.activate
    def test_table_uses_client(self):
        responses.add(
            responses.GET,
            f"{STANDINGS}/soccer/eng.1/standings",
            json={"children": []},
        )
        soccer = Soccer(league="epl")
        data = soccer.table()
        assert "children" in data

    @responses.activate
    def test_standings_delegates_to_table(self):
        responses.add(
            responses.GET,
            f"{STANDINGS}/soccer/eng.1/standings",
            json={"children": []},
        )
        soccer = Soccer(league="epl")
        data = soccer.standings()
        assert data == {"children": []}

    @responses.activate
    def test_transfers(self):
        responses.add(
            responses.GET,
            f"{CORE}/soccer/leagues/eng.1/transfers",
            json={"items": []},
        )
        soccer = Soccer(league="epl")
        data = soccer.transfers()
        assert data == {"items": []}

    @responses.activate
    def test_team_schedule_soccer(self):
        responses.add(
            responses.GET,
            f"{BASE}/soccer/all/teams/359/schedule",
            json={"events": []},
        )
        soccer = Soccer(league="epl")
        data = soccer.team_schedule("359")
        assert data == {"events": []}

    def test_list_leagues_all(self):
        leagues = Soccer.list_leagues()
        assert "epl" in leagues
        assert len(leagues) > 50

    def test_list_leagues_filtered(self):
        eng = Soccer.list_leagues("eng")
        assert all(v.startswith("eng.") for v in eng.values())
        assert "epl" in eng

    def test_list_leagues_unknown_region(self):
        result = Soccer.list_leagues("zzz")
        assert result == {}

    def test_league_resolution(self):
        s1 = Soccer(league="epl")
        assert s1.LEAGUE == "eng.1"

        s2 = Soccer(league="eng.1")
        assert s2.LEAGUE == "eng.1"

        s3 = Soccer(league="la_liga")
        assert s3.LEAGUE == "esp.1"

    @responses.activate
    def test_team_schedule_with_season_and_fixtures(self):
        responses.add(
            responses.GET,
            f"{BASE}/soccer/all/teams/359/schedule",
            json={"events": []},
        )
        Soccer(league="epl").team_schedule("359", season=2024, fixtures=True)
        url = responses.calls[0].request.url
        assert "season=2024" in url
        assert "fixture=true" in url

    @responses.activate
    def test_all_leagues_scoreboard(self):
        responses.add(
            responses.GET,
            f"{BASE}/soccer/all/scoreboard",
            json={"events": []},
        )
        data = Soccer.all_leagues_scoreboard(dates="20241201")
        assert data == {"events": []}

    @responses.activate
    def test_all_leagues_scoreboard_no_dates(self):
        responses.add(
            responses.GET,
            f"{BASE}/soccer/all/scoreboard",
            json={"events": []},
        )
        data = Soccer.all_leagues_scoreboard()
        assert data == {"events": []}

    def test_available_leagues(self):
        leagues = Soccer.available_leagues()
        assert "epl" in leagues
        assert leagues["epl"] == "eng.1"


class TestCFLUnit:
    @responses.activate
    def test_grey_cup(self):
        responses.add(
            responses.GET,
            f"{BASE}/football/cfl/rankings",
            json={"rankings": []},
        )
        data = CFL().grey_cup()
        assert data == {"rankings": []}


class TestBaseSportInheritedMethods:
    """Test BaseSport methods via XFL which doesn't override them."""

    @responses.activate
    def test_base_injuries(self):
        responses.add(responses.GET, f"{BASE}/football/xfl/injuries", json={"injuries": []})
        data = XFL().injuries()
        assert data == {"injuries": []}

    @responses.activate
    def test_base_leaders(self):
        responses.add(
            responses.GET, f"{CORE}/football/leagues/xfl/leaders", json={"categories": []}
        )
        data = XFL().leaders()
        assert data == {"categories": []}

    @responses.activate
    def test_base_leaders_with_category(self):
        responses.add(
            responses.GET, f"{CORE}/football/leagues/xfl/leaders/passing", json={"leaders": []}
        )
        data = XFL().leaders(category="passing")
        assert data == {"leaders": []}


class TestCollegeConferenceResolution:
    """Test _resolve_conference helper."""

    def test_none_returns_none(self):
        assert _resolve_conference(None, "ncaaf") is None

    def test_enum_returns_value(self):
        assert _resolve_conference(NCAAFConference.SEC, "ncaaf") == 8

    def test_int_returns_int(self):
        assert _resolve_conference(42, "ncaaf") == 42

    def test_string_looks_up(self):
        assert _resolve_conference("SEC", "ncaaf") == 8

    def test_ncaab_string(self):
        assert _resolve_conference("BIG_EAST", "ncaab") == 4

    def test_unknown_string_returns_none(self):
        assert _resolve_conference("FAKE_CONF", "ncaaf") is None

    @responses.activate
    def test_ncaaf_scoreboard_with_conference_string(self):
        responses.add(
            responses.GET,
            f"{BASE}/football/college-football/scoreboard",
            json={"events": []},
        )
        ncaaf = NCAAF()
        ncaaf.scoreboard(conference="SEC")
        assert "groups=8" in responses.calls[0].request.url

    @responses.activate
    def test_ncaab_scoreboard_with_conference_enum(self):
        responses.add(
            responses.GET,
            f"{BASE}/basketball/mens-college-basketball/scoreboard",
            json={"events": []},
        )
        ncaab = NCAAB()
        ncaab.scoreboard(conference=NCAABConference.BIG_EAST)
        assert "groups=4" in responses.calls[0].request.url
