"""Tests for convenience methods and constants."""

from datetime import date

import pytest

from espn_sports_api import (
    Conferences,
    MLBDivision,
    NBAConference,
    NCAABConference,
    NCAAFConference,
    NFLDivision,
    quick_scores,
)


class TestConferenceLookup:
    """Tests for conference/division constants."""

    def test_ncaaf_conference_enum(self):
        """Test NCAAF conference enum values."""
        assert NCAAFConference.SEC == 8
        assert NCAAFConference.BIG_TEN == 5
        assert NCAAFConference.ACC == 1

    def test_ncaab_conference_enum(self):
        """Test NCAAB conference enum values."""
        assert NCAABConference.SEC == 3
        assert NCAABConference.BIG_TEN == 7
        assert NCAABConference.BIG_EAST == 4

    def test_nfl_division_enum(self):
        """Test NFL division enum values."""
        assert NFLDivision.AFC == 1
        assert NFLDivision.NFC == 2
        assert NFLDivision.AFC_EAST == 4

    def test_nba_conference_enum(self):
        """Test NBA conference enum values."""
        assert NBAConference.EASTERN == 5
        assert NBAConference.WESTERN == 6

    def test_mlb_division_enum(self):
        """Test MLB division enum values."""
        assert MLBDivision.AMERICAN == 1
        assert MLBDivision.NATIONAL == 2

    def test_conferences_get_by_name(self):
        """Test Conferences.get() lookup by name."""
        assert Conferences.get("ncaaf", "SEC") == 8
        assert Conferences.get("ncaaf", "sec") == 8
        assert Conferences.get("ncaaf", "BIG_TEN") == 5
        assert Conferences.get("ncaaf", "Big Ten") == 5

    def test_conferences_get_unknown(self):
        """Test Conferences.get() returns None for unknown."""
        assert Conferences.get("ncaaf", "UNKNOWN") is None
        assert Conferences.get("unknown_sport", "SEC") is None

    def test_conferences_list_all(self):
        """Test Conferences.list_all() returns all conferences."""
        ncaaf = Conferences.list_all("ncaaf")
        assert isinstance(ncaaf, dict)
        assert "SEC" in ncaaf
        assert ncaaf["SEC"] == 8

    def test_conferences_list_all_unknown(self):
        """Test Conferences.list_all() returns empty for unknown sport."""
        assert Conferences.list_all("unknown") == {}


class TestConvenienceMethods:
    """Tests for date convenience methods."""

    def test_today_returns_dict(self, nfl):
        """Test today() returns scoreboard dict."""
        response = nfl.today()
        assert isinstance(response, dict)

    def test_yesterday_returns_dict(self, nfl):
        """Test yesterday() returns scoreboard dict."""
        response = nfl.yesterday()
        assert isinstance(response, dict)

    def test_tomorrow_returns_dict(self, nfl):
        """Test tomorrow() returns scoreboard dict."""
        response = nfl.tomorrow()
        assert isinstance(response, dict)

    def test_on_date_with_date_object(self, nfl):
        """Test on_date() with Python date object."""
        d = date(2024, 12, 1)
        response = nfl.on_date(d)
        assert isinstance(response, dict)

    def test_on_date_with_string(self, nfl):
        """Test on_date() with string date."""
        response = nfl.on_date("20241201")
        assert isinstance(response, dict)

    def test_date_range(self, nfl):
        """Test date_range() method."""
        start = date(2024, 12, 1)
        end = date(2024, 12, 7)
        response = nfl.date_range(start, end)
        assert isinstance(response, dict)

    def test_date_range_with_strings(self, nfl):
        """Test date_range() with string dates."""
        response = nfl.date_range("20241201", "20241207")
        assert isinstance(response, dict)

    def test_live_filters_events(self, nfl):
        """Test live() filters to in-progress games."""
        response = nfl.live()
        assert isinstance(response, dict)
        assert "events" in response

    def test_for_week(self, nfl):
        """Test for_week() gets specific week."""
        response = nfl.for_week(1)
        assert isinstance(response, dict)


class TestCollegeConferenceFiltering:
    """Tests for college sports conference filtering."""

    def test_ncaaf_scoreboard_with_string_conference(self, ncaaf):
        """Test NCAAF scoreboard with conference string."""
        response = ncaaf.scoreboard(conference="SEC")
        assert isinstance(response, dict)

    def test_ncaaf_scoreboard_with_enum(self, ncaaf):
        """Test NCAAF scoreboard with conference enum."""
        response = ncaaf.scoreboard(conference=NCAAFConference.BIG_TEN)
        assert isinstance(response, dict)

    def test_ncaaf_scoreboard_with_int(self, ncaaf):
        """Test NCAAF scoreboard with conference ID."""
        response = ncaaf.scoreboard(conference=8)
        assert isinstance(response, dict)

    def test_ncaab_scoreboard_with_string_conference(self, ncaab):
        """Test NCAAB scoreboard with conference string."""
        response = ncaab.scoreboard(conference="BIG_EAST")
        assert isinstance(response, dict)

    def test_ncaab_scoreboard_with_enum(self, ncaab):
        """Test NCAAB scoreboard with conference enum."""
        response = ncaab.scoreboard(conference=NCAABConference.SEC)
        assert isinstance(response, dict)


class TestQuickScores:
    """Tests for quick_scores() function."""

    def test_quick_scores_nfl(self):
        """Test quick_scores() for NFL."""
        response = quick_scores("nfl")
        assert isinstance(response, dict)

    def test_quick_scores_nba(self):
        """Test quick_scores() for NBA."""
        response = quick_scores("nba")
        assert isinstance(response, dict)

    def test_quick_scores_default(self):
        """Test quick_scores() defaults to NFL."""
        response = quick_scores()
        assert isinstance(response, dict)

    def test_quick_scores_case_insensitive(self):
        """Test quick_scores() is case insensitive."""
        response = quick_scores("NBA")
        assert isinstance(response, dict)

    def test_quick_scores_mls(self):
        """Test quick_scores() for MLS (soccer)."""
        response = quick_scores("mls")
        assert isinstance(response, dict)

    def test_quick_scores_unknown_raises(self):
        """Test quick_scores() raises for unknown sport."""
        with pytest.raises(ValueError, match="Unknown sport"):
            quick_scores("unknown_sport")
