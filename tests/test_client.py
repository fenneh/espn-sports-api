"""Tests for ESPN client."""

from espn_sports_api import ESPNClient


class TestESPNClient:
    """Tests for ESPNClient class."""

    def test_client_init(self):
        client = ESPNClient()
        assert client.timeout == 30
        assert client.session is not None

    def test_client_custom_timeout(self):
        client = ESPNClient(timeout=60)
        assert client.timeout == 60

    def test_client_context_manager(self):
        with ESPNClient() as client:
            assert client.session is not None

    def test_client_has_required_urls(self):
        assert ESPNClient.BASE_URL == "https://site.api.espn.com/apis/site/v2/sports/"
        assert ESPNClient.CORE_URL == "https://sports.core.api.espn.com/v2/sports/"
        assert ESPNClient.WEB_URL == "https://site.web.api.espn.com/apis/common/v3/sports/"
        assert ESPNClient.FANTASY_URL == "https://lm-api-reads.fantasy.espn.com/apis/v3/"
        assert ESPNClient.NOW_URL == "https://now.core.api.espn.com/v1/"
        assert ESPNClient.GAMBIT_URL == "https://gambit-api.fantasy.espn.com/apis/v1/"
        assert ESPNClient.STANDINGS_URL == "https://site.api.espn.com/apis/v2/sports/"
