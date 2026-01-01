"""Tests for ESPN client."""

import pytest

from espn_sports_api import ESPNClient


class TestESPNClient:
    """Tests for ESPNClient class."""

    def test_client_init(self):
        """Test client initialization."""
        client = ESPNClient()
        assert client.timeout == 30
        assert client.session is not None

    def test_client_custom_timeout(self):
        """Test client with custom timeout."""
        client = ESPNClient(timeout=60)
        assert client.timeout == 60

    def test_client_context_manager(self):
        """Test client as context manager."""
        with ESPNClient() as client:
            assert client.session is not None

    def test_client_has_required_urls(self):
        """Test client has all required base URLs."""
        assert ESPNClient.BASE_URL == "https://site.api.espn.com/apis/site/v2/sports/"
        assert ESPNClient.CORE_URL == "https://sports.core.api.espn.com/v2/sports/"
        assert ESPNClient.WEB_URL == "https://site.web.api.espn.com/apis/common/v3/sports/"
        assert ESPNClient.FANTASY_URL == "https://lm-api-reads.fantasy.espn.com/apis/v3/"


class TestClientIntegration:
    """Integration tests that hit the actual API."""

    def test_get_nfl_scoreboard(self, client):
        """Test fetching NFL scoreboard."""
        response = client.get("football/nfl/scoreboard")
        assert "events" in response or "leagues" in response

    def test_get_nfl_teams(self, client):
        """Test fetching NFL teams."""
        response = client.get("football/nfl/teams")
        assert "sports" in response

    def test_get_core_athletes(self, client):
        """Test fetching athletes from core API."""
        response = client.get_core("football/leagues/nfl/athletes?limit=5")
        assert "items" in response or "count" in response

    def test_invalid_endpoint_raises(self, client):
        """Test that invalid endpoint raises error."""
        with pytest.raises(Exception):
            client.get("invalid/endpoint/that/does/not/exist")
