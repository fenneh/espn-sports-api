"""Unit tests for sport-specific methods with mocked HTTP responses.

Each test verifies:
1. The correct ESPN endpoint URL is called (via responses strict matching)
2. Parameters are passed through correctly
3. The mock response data is returned unchanged
"""

import responses

from espn_sports_api import (
    MLB,
    NBA,
    NCAAB,
    NCAAF,
    NFL,
    NHL,
    UFC,
    WNBA,
    CollegeBaseball,
    Golf,
    Racing,
    Tennis,
    WomensNCAAB,
)

BASE = "https://site.api.espn.com/apis/site/v2/sports"
CORE = "https://sports.core.api.espn.com/v2/sports"


class TestNFLMethods:
    @responses.activate
    def test_draft_hits_core_draft_endpoint(self):
        responses.add(
            responses.GET,
            f"{CORE}/football/leagues/nfl/draft",
            json={"rounds": [{"picks": []}]},
        )
        data = NFL().draft()
        assert data == {"rounds": [{"picks": []}]}
        assert len(responses.calls) == 1

    @responses.activate
    def test_draft_passes_year_param(self):
        responses.add(responses.GET, f"{CORE}/football/leagues/nfl/draft", json={"year": 2024})
        data = NFL().draft(year=2024)
        assert "year=2024" in responses.calls[0].request.url
        assert data["year"] == 2024

    @responses.activate
    def test_draft_omits_year_when_none(self):
        responses.add(responses.GET, f"{CORE}/football/leagues/nfl/draft", json={})
        NFL().draft()
        assert "year" not in (responses.calls[0].request.url or "")

    @responses.activate
    def test_depth_charts_includes_team_id_in_path(self):
        responses.add(
            responses.GET,
            f"{CORE}/football/leagues/nfl/teams/ne/depthcharts",
            json={"positions": ["QB", "RB"]},
        )
        data = NFL().depth_charts("ne")
        assert data["positions"] == ["QB", "RB"]

    @responses.activate
    def test_injuries_uses_site_api_not_core(self):
        mock_data = {"injuries": [{"name": "Player X", "status": "Out"}]}
        responses.add(responses.GET, f"{BASE}/football/nfl/injuries", json=mock_data)
        data = NFL().injuries()
        assert data == mock_data

    @responses.activate
    def test_leaders_without_category_hits_base_leaders_url(self):
        responses.add(
            responses.GET, f"{CORE}/football/leagues/nfl/leaders", json={"categories": ["passing"]}
        )
        data = NFL().leaders()
        assert data["categories"] == ["passing"]
        assert responses.calls[0].request.url.split("?")[0].endswith("/leaders")

    @responses.activate
    def test_leaders_with_category_appends_to_url(self):
        responses.add(
            responses.GET,
            f"{CORE}/football/leagues/nfl/leaders/passing",
            json={"leaders": [{"name": "Mahomes"}]},
        )
        data = NFL().leaders(category="passing")
        assert data["leaders"][0]["name"] == "Mahomes"


class TestNBAMethods:
    @responses.activate
    def test_draft_hits_core_endpoint(self):
        responses.add(
            responses.GET, f"{CORE}/basketball/leagues/nba/draft", json={"picks": [1, 2, 3]}
        )
        assert NBA().draft()["picks"] == [1, 2, 3]

    @responses.activate
    def test_draft_passes_year_param(self):
        responses.add(responses.GET, f"{CORE}/basketball/leagues/nba/draft", json={})
        NBA().draft(year=2023)
        assert "year=2023" in responses.calls[0].request.url

    @responses.activate
    def test_leaders_without_category(self):
        responses.add(
            responses.GET,
            f"{CORE}/basketball/leagues/nba/leaders",
            json={"categories": ["points"]},
        )
        assert NBA().leaders()["categories"] == ["points"]

    @responses.activate
    def test_leaders_appends_category_to_path(self):
        responses.add(
            responses.GET,
            f"{CORE}/basketball/leagues/nba/leaders/points",
            json={"leaders": [{"name": "Jokic"}]},
        )
        data = NBA().leaders(category="points")
        assert data["leaders"][0]["name"] == "Jokic"

    @responses.activate
    def test_free_agents_hits_freeagents_endpoint(self):
        responses.add(
            responses.GET,
            f"{CORE}/basketball/leagues/nba/freeagents",
            json={"count": 42, "items": []},
        )
        data = NBA().free_agents()
        assert data["count"] == 42

    @responses.activate
    def test_transactions_hits_transactions_endpoint(self):
        responses.add(
            responses.GET,
            f"{CORE}/basketball/leagues/nba/transactions",
            json={"count": 5, "items": []},
        )
        assert NBA().transactions()["count"] == 5


class TestMLBMethods:
    @responses.activate
    def test_draft_returns_mock_data(self):
        responses.add(
            responses.GET, f"{CORE}/baseball/leagues/mlb/draft", json={"year": 2024, "rounds": []}
        )
        assert MLB().draft()["year"] == 2024

    @responses.activate
    def test_draft_passes_year_param(self):
        responses.add(responses.GET, f"{CORE}/baseball/leagues/mlb/draft", json={})
        MLB().draft(year=2024)
        assert "year=2024" in responses.calls[0].request.url

    @responses.activate
    def test_leaders_without_category(self):
        responses.add(
            responses.GET,
            f"{CORE}/baseball/leagues/mlb/leaders",
            json={"categories": ["batting"]},
        )
        assert "batting" in MLB().leaders()["categories"]

    @responses.activate
    def test_leaders_with_category(self):
        responses.add(
            responses.GET,
            f"{CORE}/baseball/leagues/mlb/leaders/batting",
            json={"leaders": [{"name": "Ohtani"}]},
        )
        assert MLB().leaders(category="batting")["leaders"][0]["name"] == "Ohtani"

    @responses.activate
    def test_free_agents(self):
        responses.add(responses.GET, f"{CORE}/baseball/leagues/mlb/freeagents", json={"count": 100})
        assert MLB().free_agents()["count"] == 100

    @responses.activate
    def test_transactions(self):
        responses.add(responses.GET, f"{CORE}/baseball/leagues/mlb/transactions", json={"count": 7})
        assert MLB().transactions()["count"] == 7


class TestNHLMethods:
    @responses.activate
    def test_draft(self):
        responses.add(
            responses.GET, f"{CORE}/hockey/leagues/nhl/draft", json={"year": 2024, "rounds": []}
        )
        assert NHL().draft()["year"] == 2024

    @responses.activate
    def test_draft_passes_year_param(self):
        responses.add(responses.GET, f"{CORE}/hockey/leagues/nhl/draft", json={})
        NHL().draft(year=2024)
        assert "year=2024" in responses.calls[0].request.url

    @responses.activate
    def test_leaders_without_category(self):
        responses.add(
            responses.GET, f"{CORE}/hockey/leagues/nhl/leaders", json={"categories": ["goals"]}
        )
        assert NHL().leaders()["categories"] == ["goals"]

    @responses.activate
    def test_leaders_with_category(self):
        responses.add(
            responses.GET,
            f"{CORE}/hockey/leagues/nhl/leaders/goals",
            json={"leaders": [{"name": "Ovechkin"}]},
        )
        assert NHL().leaders(category="goals")["leaders"][0]["name"] == "Ovechkin"

    @responses.activate
    def test_free_agents(self):
        responses.add(responses.GET, f"{CORE}/hockey/leagues/nhl/freeagents", json={"count": 50})
        assert NHL().free_agents()["count"] == 50

    @responses.activate
    def test_transactions(self):
        responses.add(responses.GET, f"{CORE}/hockey/leagues/nhl/transactions", json={"count": 3})
        assert NHL().transactions()["count"] == 3


class TestWNBAMethods:
    """WNBA uses _endpoint() not _core_endpoint() — no /leagues/ in path."""

    @responses.activate
    def test_draft_uses_endpoint_not_core_endpoint(self):
        responses.add(
            responses.GET, f"{CORE}/basketball/wnba/draft", json={"year": 2024, "picks": []}
        )
        assert WNBA().draft()["year"] == 2024

    @responses.activate
    def test_draft_passes_year_param(self):
        responses.add(responses.GET, f"{CORE}/basketball/wnba/draft", json={})
        WNBA().draft(year=2024)
        assert "year=2024" in responses.calls[0].request.url

    @responses.activate
    def test_leaders_without_category(self):
        responses.add(
            responses.GET, f"{CORE}/basketball/wnba/leaders", json={"categories": ["points"]}
        )
        assert WNBA().leaders()["categories"] == ["points"]

    @responses.activate
    def test_leaders_with_category(self):
        responses.add(
            responses.GET,
            f"{CORE}/basketball/wnba/leaders/points",
            json={"leaders": [{"name": "Clark"}]},
        )
        assert WNBA().leaders(category="points")["leaders"][0]["name"] == "Clark"

    @responses.activate
    def test_transactions(self):
        responses.add(responses.GET, f"{CORE}/basketball/wnba/transactions", json={"count": 2})
        assert WNBA().transactions()["count"] == 2


class TestUFCMethods:
    @responses.activate
    def test_rankings_without_division(self):
        responses.add(
            responses.GET,
            f"{CORE}/mma/leagues/ufc/rankings",
            json={"divisions": ["lightweight"]},
        )
        assert UFC().rankings()["divisions"] == ["lightweight"]
        assert responses.calls[0].request.url.split("?")[0].endswith("/rankings")

    @responses.activate
    def test_rankings_appends_division_to_path(self):
        responses.add(
            responses.GET,
            f"{CORE}/mma/leagues/ufc/rankings/lightweight",
            json={"athletes": [{"name": "Makhachev"}]},
        )
        data = UFC().rankings(division="lightweight")
        assert data["athletes"][0]["name"] == "Makhachev"

    @responses.activate
    def test_events_without_limit(self):
        responses.add(
            responses.GET, f"{CORE}/mma/leagues/ufc/events", json={"count": 10, "items": []}
        )
        assert UFC().events()["count"] == 10
        assert "limit" not in (responses.calls[0].request.url or "")

    @responses.activate
    def test_events_passes_limit_param(self):
        responses.add(responses.GET, f"{CORE}/mma/leagues/ufc/events", json={"items": []})
        UFC().events(limit=5)
        assert "limit=5" in responses.calls[0].request.url

    @responses.activate
    def test_event_details_includes_event_id_in_path(self):
        responses.add(
            responses.GET,
            f"{CORE}/mma/leagues/ufc/events/12345",
            json={"id": "12345", "name": "UFC 300"},
        )
        data = UFC().event_details("12345")
        assert data["id"] == "12345"
        assert data["name"] == "UFC 300"

    @responses.activate
    def test_fighter_delegates_to_athlete(self):
        responses.add(
            responses.GET,
            f"{CORE}/mma/leagues/ufc/athletes/54321",
            json={"id": "54321", "displayName": "Test Fighter"},
        )
        data = UFC().fighter("54321")
        assert data["displayName"] == "Test Fighter"


class TestGolfMethods:
    @responses.activate
    def test_leaderboard_uses_site_api_scoreboard(self):
        responses.add(
            responses.GET,
            f"{BASE}/golf/pga/scoreboard",
            json={"events": [{"name": "The Masters"}]},
        )
        data = Golf().leaderboard()
        assert data["events"][0]["name"] == "The Masters"
        assert "event=" not in (responses.calls[0].request.url or "")

    @responses.activate
    def test_leaderboard_passes_event_id_param(self):
        responses.add(responses.GET, f"{BASE}/golf/pga/scoreboard", json={"events": []})
        Golf().leaderboard(event_id="401580")
        assert "event=401580" in responses.calls[0].request.url

    @responses.activate
    def test_rankings_hits_core_rankings(self):
        responses.add(
            responses.GET,
            f"{CORE}/golf/leagues/pga/rankings",
            json={"rankings": [{"rank": 1}]},
        )
        assert Golf().rankings()["rankings"][0]["rank"] == 1

    @responses.activate
    def test_schedule_hits_core_events(self):
        responses.add(
            responses.GET,
            f"{CORE}/golf/leagues/pga/events",
            json={"items": [{"name": "PGA Championship"}]},
        )
        assert Golf().schedule()["items"][0]["name"] == "PGA Championship"

    @responses.activate
    def test_schedule_passes_season_param(self):
        responses.add(responses.GET, f"{CORE}/golf/leagues/pga/events", json={"items": []})
        Golf().schedule(season=2024)
        assert "season=2024" in responses.calls[0].request.url

    @responses.activate
    def test_player_delegates_to_athlete(self):
        responses.add(
            responses.GET,
            f"{CORE}/golf/leagues/pga/athletes/1234",
            json={"id": "1234", "displayName": "Tiger Woods"},
        )
        assert Golf().player("1234")["displayName"] == "Tiger Woods"

    def test_tour_selection_maps_known_tours(self):
        assert Golf(tour="lpga").LEAGUE == "lpga"
        assert Golf(tour="european").LEAGUE == "eur"
        assert Golf(tour="champions").LEAGUE == "champ"

    def test_tour_selection_passes_unknown_through(self):
        assert Golf(tour="custom").LEAGUE == "custom"


class TestRacingMethods:
    @responses.activate
    def test_schedule_hits_core_events(self):
        responses.add(
            responses.GET,
            f"{CORE}/racing/leagues/f1/events",
            json={"items": [{"name": "Monaco GP"}]},
        )
        assert Racing().schedule()["items"][0]["name"] == "Monaco GP"

    @responses.activate
    def test_schedule_passes_season_param(self):
        responses.add(responses.GET, f"{CORE}/racing/leagues/f1/events", json={"items": []})
        Racing().schedule(season=2024)
        assert "season=2024" in responses.calls[0].request.url

    @responses.activate
    def test_standings_uses_site_api(self):
        responses.add(
            responses.GET,
            f"{BASE}/racing/f1/standings",
            json={"driver": [{"name": "Verstappen"}]},
        )
        assert Racing().standings()["driver"][0]["name"] == "Verstappen"

    @responses.activate
    def test_standings_passes_season_param(self):
        responses.add(responses.GET, f"{BASE}/racing/f1/standings", json={})
        Racing().standings(season=2024)
        assert "season=2024" in responses.calls[0].request.url

    @responses.activate
    def test_results_delegates_to_event(self):
        responses.add(
            responses.GET,
            f"{BASE}/racing/f1/summary",
            json={"header": {"competitions": []}},
        )
        data = Racing().results("401580")
        assert "header" in data
        assert "event=401580" in responses.calls[0].request.url

    @responses.activate
    def test_driver_delegates_to_athlete(self):
        responses.add(
            responses.GET,
            f"{CORE}/racing/leagues/f1/athletes/4665",
            json={"id": "4665", "displayName": "Hamilton"},
        )
        assert Racing().driver("4665")["displayName"] == "Hamilton"

    def test_available_series_returns_copy_of_series_dict(self):
        series = Racing.available_series()
        expected = {
            "f1": "f1",
            "formula1": "f1",
            "nascar": "nascar",
            "nascar_cup": "nascar",
            "indycar": "irl",
        }
        assert series == expected
        series["test"] = "test"
        assert "test" not in Racing.available_series()

    def test_series_selection_maps_known_series(self):
        assert Racing(series="nascar").LEAGUE == "nascar"
        assert Racing(series="indycar").LEAGUE == "irl"
        assert Racing(series="formula1").LEAGUE == "f1"

    def test_series_selection_passes_unknown_through(self):
        assert Racing(series="wrc").LEAGUE == "wrc"


class TestTennisMethods:
    @responses.activate
    def test_rankings_hits_core_rankings(self):
        responses.add(
            responses.GET,
            f"{CORE}/tennis/leagues/atp/rankings",
            json={"rankings": [{"athlete": "Sinner"}]},
        )
        assert Tennis().rankings()["rankings"][0]["athlete"] == "Sinner"

    @responses.activate
    def test_schedule_hits_core_events(self):
        responses.add(
            responses.GET,
            f"{CORE}/tennis/leagues/atp/events",
            json={"items": [{"name": "Wimbledon"}]},
        )
        assert Tennis().schedule()["items"][0]["name"] == "Wimbledon"

    @responses.activate
    def test_schedule_passes_season_param(self):
        responses.add(responses.GET, f"{CORE}/tennis/leagues/atp/events", json={"items": []})
        Tennis().schedule(season=2024)
        assert "season=2024" in responses.calls[0].request.url

    @responses.activate
    def test_tournament_delegates_to_event(self):
        responses.add(
            responses.GET,
            f"{BASE}/tennis/atp/summary",
            json={"header": {"name": "US Open"}},
        )
        data = Tennis().tournament("401580")
        assert data["header"]["name"] == "US Open"
        assert "event=401580" in responses.calls[0].request.url

    @responses.activate
    def test_player_delegates_to_athlete(self):
        responses.add(
            responses.GET,
            f"{CORE}/tennis/leagues/atp/athletes/1234",
            json={"id": "1234", "displayName": "Djokovic"},
        )
        assert Tennis().player("1234")["displayName"] == "Djokovic"

    def test_tour_selection(self):
        assert Tennis(tour="wta").LEAGUE == "wta"
        assert Tennis(tour="atp").LEAGUE == "atp"


class TestNCAAFMethods:
    @responses.activate
    def test_conferences_hits_core_groups(self):
        responses.add(
            responses.GET,
            f"{CORE}/football/leagues/college-football/groups",
            json={"items": [{"name": "SEC"}]},
        )
        assert NCAAF().conferences()["items"][0]["name"] == "SEC"

    @responses.activate
    def test_recruiting_without_year(self):
        responses.add(
            responses.GET,
            f"{CORE}/football/leagues/college-football/recruiting",
            json={"items": [{"class": 2025}]},
        )
        data = NCAAF().recruiting()
        assert data["items"][0]["class"] == 2025
        assert "year" not in (responses.calls[0].request.url or "")

    @responses.activate
    def test_recruiting_passes_year_param(self):
        responses.add(
            responses.GET,
            f"{CORE}/football/leagues/college-football/recruiting",
            json={"items": []},
        )
        NCAAF().recruiting(year=2024)
        assert "year=2024" in responses.calls[0].request.url

    @responses.activate
    def test_rankings_uses_site_api(self):
        responses.add(
            responses.GET,
            f"{BASE}/football/college-football/rankings",
            json={"rankings": [{"name": "AP Top 25"}]},
        )
        assert NCAAF().rankings()["rankings"][0]["name"] == "AP Top 25"


class TestNCAABMethods:
    @responses.activate
    def test_bracket_without_season(self):
        responses.add(
            responses.GET,
            f"{BASE}/basketball/mens-college-basketball/tournament",
            json={"bracket": [{"region": "East"}]},
        )
        assert NCAAB().bracket()["bracket"][0]["region"] == "East"
        assert "season" not in (responses.calls[0].request.url or "")

    @responses.activate
    def test_bracket_passes_season_param(self):
        responses.add(
            responses.GET,
            f"{BASE}/basketball/mens-college-basketball/tournament",
            json={"bracket": []},
        )
        NCAAB().bracket(season=2024)
        assert "season=2024" in responses.calls[0].request.url

    @responses.activate
    def test_weeks_builds_correct_nested_path(self):
        responses.add(
            responses.GET,
            f"{CORE}/basketball/leagues/mens-college-basketball/seasons/2024/types/2/weeks",
            json={"items": [{"number": 1}]},
        )
        data = NCAAB().weeks(season=2024)
        assert data["items"][0]["number"] == 1

    @responses.activate
    def test_weeks_respects_season_type_param(self):
        responses.add(
            responses.GET,
            f"{CORE}/basketball/leagues/mens-college-basketball/seasons/2024/types/3/weeks",
            json={"items": []},
        )
        NCAAB().weeks(season=2024, season_type=3)
        assert "/types/3/" in responses.calls[0].request.url

    @responses.activate
    def test_rankings_uses_site_api(self):
        responses.add(
            responses.GET,
            f"{BASE}/basketball/mens-college-basketball/rankings",
            json={"rankings": [{"name": "AP"}]},
        )
        assert NCAAB().rankings()["rankings"][0]["name"] == "AP"

    @responses.activate
    def test_conferences_hits_core_groups(self):
        responses.add(
            responses.GET,
            f"{CORE}/basketball/leagues/mens-college-basketball/groups",
            json={"items": [{"name": "Big East"}]},
        )
        assert NCAAB().conferences()["items"][0]["name"] == "Big East"


class TestWomensNCAABMethods:
    @responses.activate
    def test_rankings_uses_site_api(self):
        responses.add(
            responses.GET,
            f"{BASE}/basketball/womens-college-basketball/rankings",
            json={"rankings": [{"name": "AP"}]},
        )
        assert WomensNCAAB().rankings()["rankings"][0]["name"] == "AP"

    @responses.activate
    def test_bracket_without_season(self):
        responses.add(
            responses.GET,
            f"{BASE}/basketball/womens-college-basketball/tournament",
            json={"bracket": [{"region": "West"}]},
        )
        assert WomensNCAAB().bracket()["bracket"][0]["region"] == "West"

    @responses.activate
    def test_bracket_passes_season_param(self):
        responses.add(
            responses.GET,
            f"{BASE}/basketball/womens-college-basketball/tournament",
            json={"bracket": []},
        )
        WomensNCAAB().bracket(season=2024)
        assert "season=2024" in responses.calls[0].request.url


class TestCollegeBaseballMethods:
    @responses.activate
    def test_rankings_uses_site_api(self):
        responses.add(
            responses.GET,
            f"{BASE}/baseball/college-baseball/rankings",
            json={"rankings": [{"name": "D1 Baseball"}]},
        )
        assert CollegeBaseball().rankings()["rankings"][0]["name"] == "D1 Baseball"

    @responses.activate
    def test_conferences_hits_core_groups(self):
        responses.add(
            responses.GET,
            f"{CORE}/baseball/leagues/college-baseball/groups",
            json={"items": [{"name": "SEC"}]},
        )
        assert CollegeBaseball().conferences()["items"][0]["name"] == "SEC"
