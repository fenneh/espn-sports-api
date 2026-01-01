"""Integration tests for sport modules.

These tests hit the actual ESPN API to verify endpoints are working.
If ESPN changes their API, these tests will fail.
"""


class TestNFL:
    """Tests for NFL module."""

    def test_scoreboard(self, nfl):
        """Test NFL scoreboard endpoint."""
        response = nfl.scoreboard()
        assert isinstance(response, dict)
        # Should have events or leagues key
        assert "events" in response or "leagues" in response

    def test_scoreboard_with_dates(self, nfl):
        """Test NFL scoreboard with date filter."""
        response = nfl.scoreboard(dates="20241201")
        assert isinstance(response, dict)

    def test_teams(self, nfl):
        """Test NFL teams endpoint."""
        response = nfl.teams()
        assert "sports" in response

    def test_team(self, nfl):
        """Test NFL single team endpoint."""
        response = nfl.team("ne")  # Patriots
        assert "team" in response

    def test_news(self, nfl):
        """Test NFL news endpoint."""
        response = nfl.news(limit=5)
        assert "articles" in response or "header" in response

    def test_standings(self, nfl):
        """Test NFL standings endpoint."""
        response = nfl.standings()
        assert isinstance(response, dict)

    def test_injuries(self, nfl):
        """Test NFL league-wide injuries endpoint."""
        response = nfl.injuries()
        assert isinstance(response, dict)

    def test_statistics(self, nfl):
        """Test NFL statistics endpoint."""
        response = nfl.statistics()
        assert isinstance(response, dict)


class TestNBA:
    """Tests for NBA module."""

    def test_scoreboard(self, nba):
        """Test NBA scoreboard endpoint."""
        response = nba.scoreboard()
        assert isinstance(response, dict)

    def test_teams(self, nba):
        """Test NBA teams endpoint."""
        response = nba.teams()
        assert "sports" in response

    def test_team(self, nba):
        """Test NBA single team endpoint."""
        response = nba.team("lal")  # Lakers
        assert "team" in response


class TestMLB:
    """Tests for MLB module."""

    def test_scoreboard(self, mlb):
        """Test MLB scoreboard endpoint."""
        response = mlb.scoreboard()
        assert isinstance(response, dict)

    def test_teams(self, mlb):
        """Test MLB teams endpoint."""
        response = mlb.teams()
        assert "sports" in response


class TestNHL:
    """Tests for NHL module."""

    def test_scoreboard(self, nhl):
        """Test NHL scoreboard endpoint."""
        response = nhl.scoreboard()
        assert isinstance(response, dict)

    def test_teams(self, nhl):
        """Test NHL teams endpoint."""
        response = nhl.teams()
        assert "sports" in response


class TestSoccer:
    """Tests for Soccer module."""

    def test_scoreboard(self, soccer):
        """Test Soccer scoreboard endpoint."""
        response = soccer.scoreboard()
        assert isinstance(response, dict)

    def test_teams(self, soccer):
        """Test Soccer teams endpoint."""
        response = soccer.teams()
        assert "sports" in response

    def test_standings(self, soccer):
        """Test Soccer standings/table endpoint."""
        response = soccer.table()
        assert isinstance(response, dict)

    def test_available_leagues(self):
        """Test available leagues returns dict."""
        from espn_sports_api import Soccer

        leagues = Soccer.available_leagues()
        assert isinstance(leagues, dict)
        assert "epl" in leagues
        assert "champions_league" in leagues
        assert len(leagues) > 50  # We added 90+ leagues

    def test_different_leagues(self):
        """Test instantiating different leagues."""
        from espn_sports_api import Soccer

        leagues_to_test = ["la_liga", "bundesliga", "mls"]
        for league in leagues_to_test:
            s = Soccer(league=league)
            assert s.LEAGUE != "eng.1"  # Not default


class TestUFC:
    """Tests for UFC module."""

    def test_scoreboard(self, ufc):
        """Test UFC scoreboard endpoint."""
        response = ufc.scoreboard()
        assert isinstance(response, dict)


class TestGolf:
    """Tests for Golf module."""

    def test_scoreboard(self, golf):
        """Test Golf scoreboard endpoint."""
        response = golf.scoreboard()
        assert isinstance(response, dict)


class TestRacing:
    """Tests for Racing module."""

    def test_scoreboard(self, racing):
        """Test Racing scoreboard endpoint."""
        response = racing.scoreboard()
        assert isinstance(response, dict)

    def test_different_series(self):
        """Test instantiating different racing series."""
        from espn_sports_api import Racing

        f1 = Racing(series="f1")
        nascar = Racing(series="nascar")

        assert f1.LEAGUE == "f1"
        assert nascar.LEAGUE == "nascar"


class TestTennis:
    """Tests for Tennis module."""

    def test_scoreboard(self, tennis):
        """Test Tennis scoreboard endpoint."""
        response = tennis.scoreboard()
        assert isinstance(response, dict)


class TestNCAAF:
    """Tests for NCAAF module."""

    def test_scoreboard(self, ncaaf):
        """Test NCAAF scoreboard endpoint."""
        response = ncaaf.scoreboard()
        assert isinstance(response, dict)

    def test_rankings(self, ncaaf):
        """Test NCAAF rankings endpoint."""
        response = ncaaf.rankings()
        assert isinstance(response, dict)


class TestNCAAB:
    """Tests for NCAAB module."""

    def test_scoreboard(self, ncaab):
        """Test NCAAB scoreboard endpoint."""
        response = ncaab.scoreboard()
        assert isinstance(response, dict)


class TestCFLAndXFL:
    """Tests for CFL and XFL modules."""

    def test_cfl_import(self):
        """Test CFL can be imported."""
        from espn_sports_api import CFL

        cfl = CFL()
        assert cfl.SPORT == "football"
        assert cfl.LEAGUE == "cfl"

    def test_xfl_import(self):
        """Test XFL can be imported."""
        from espn_sports_api import XFL

        xfl = XFL()
        assert xfl.SPORT == "football"
        assert xfl.LEAGUE == "xfl"


class TestCommonMethods:
    """Test common methods across all sports."""

    def test_context_manager(self, nfl):
        """Test sport module as context manager."""
        from espn_sports_api import NFL

        with NFL() as sport:
            response = sport.teams()
            assert "sports" in response

    def test_athletes(self, nfl):
        """Test athletes endpoint."""
        response = nfl.athletes(limit=5)
        assert isinstance(response, dict)

    def test_seasons(self, nfl):
        """Test seasons endpoint."""
        response = nfl.seasons(2024)
        assert isinstance(response, dict)
