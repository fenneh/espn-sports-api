"""Tests for fantasy sports module."""

from espn_sports_api import (
    FantasyBaseball,
    FantasyBasketball,
    FantasyFootball,
    FantasyHockey,
    FantasyLeague,
)


class TestFantasyClasses:
    """Test fantasy class initialization."""

    def test_fantasy_football_init(self):
        """Test FantasyFootball initialization."""
        league = FantasyFootball(league_id=123456, season=2024)
        assert league.sport == "ffl"
        assert league.league_id == 123456
        assert league.season == 2024

    def test_fantasy_basketball_init(self):
        """Test FantasyBasketball initialization."""
        league = FantasyBasketball(league_id=123456, season=2024)
        assert league.sport == "fba"

    def test_fantasy_baseball_init(self):
        """Test FantasyBaseball initialization."""
        league = FantasyBaseball(league_id=123456, season=2024)
        assert league.sport == "flb"

    def test_fantasy_hockey_init(self):
        """Test FantasyHockey initialization."""
        league = FantasyHockey(league_id=123456, season=2024)
        assert league.sport == "fhl"

    def test_fantasy_league_base_init(self):
        """Test base FantasyLeague initialization."""
        league = FantasyLeague(
            sport="ffl",
            league_id=123456,
            season=2024,
        )
        assert league.sport == "ffl"

    def test_fantasy_league_with_cookies(self):
        """Test FantasyLeague with authentication cookies."""
        league = FantasyLeague(
            sport="ffl",
            league_id=123456,
            season=2024,
            swid="{TEST-SWID}",
            espn_s2="TEST_S2_COOKIE",
        )
        # Verify cookies were set
        cookies = league.client.session.cookies
        assert cookies.get("SWID") == "{TEST-SWID}"
        assert cookies.get("espn_s2") == "TEST_S2_COOKIE"

    def test_fantasy_context_manager(self):
        """Test fantasy league as context manager."""
        with FantasyFootball(league_id=123456, season=2024) as league:
            assert league.sport == "ffl"

    def test_fantasy_endpoint_building(self):
        """Test endpoint path construction."""
        league = FantasyFootball(league_id=123456, season=2024)
        endpoint = league._endpoint()
        assert "ffl" in endpoint
        assert "2024" in endpoint
        assert "123456" in endpoint
