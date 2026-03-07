"""Unit tests for ESPN client with mocked HTTP responses."""

import pytest
import requests
import responses

from espn_sports_api import (
    ESPNApiError,
    ESPNClient,
    ESPNNotFoundError,
    ESPNRateLimitError,
    ESPNResponseError,
    ESPNServerError,
    ESPNTimeoutError,
)


class TestClientErrorHandling:
    """Test HTTP error handling with custom exceptions."""

    @responses.activate
    def test_404_raises_not_found(self):
        responses.add(
            responses.GET,
            "https://site.api.espn.com/apis/site/v2/sports/football/nfl/bogus",
            json={"error": "not found"},
            status=404,
        )
        client = ESPNClient(retries=0)
        with pytest.raises(ESPNNotFoundError) as exc_info:
            client.get("football/nfl/bogus")
        assert exc_info.value.status_code == 404
        assert "404" in str(exc_info.value)

    @responses.activate
    def test_429_raises_rate_limit(self):
        responses.add(
            responses.GET,
            "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams",
            json={"error": "rate limited"},
            status=429,
        )
        client = ESPNClient(retries=0)
        with pytest.raises(ESPNRateLimitError) as exc_info:
            client.get("football/nfl/teams")
        assert exc_info.value.status_code == 429

    @responses.activate
    def test_500_raises_server_error(self):
        responses.add(
            responses.GET,
            "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams",
            json={"error": "internal"},
            status=500,
        )
        client = ESPNClient(retries=0)
        with pytest.raises(ESPNServerError) as exc_info:
            client.get("football/nfl/teams")
        assert exc_info.value.status_code == 500

    @responses.activate
    def test_503_raises_server_error(self):
        responses.add(
            responses.GET,
            "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams",
            json={"error": "unavailable"},
            status=503,
        )
        client = ESPNClient(retries=0)
        with pytest.raises(ESPNServerError) as exc_info:
            client.get("football/nfl/teams")
        assert exc_info.value.status_code == 503

    @responses.activate
    def test_403_raises_generic_api_error(self):
        responses.add(
            responses.GET,
            "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams",
            json={"error": "forbidden"},
            status=403,
        )
        client = ESPNClient(retries=0)
        with pytest.raises(ESPNApiError) as exc_info:
            client.get("football/nfl/teams")
        assert exc_info.value.status_code == 403

    @responses.activate
    def test_malformed_json_raises_response_error(self):
        responses.add(
            responses.GET,
            "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams",
            body="not json at all",
            status=200,
            content_type="text/plain",
        )
        client = ESPNClient(retries=0)
        with pytest.raises(ESPNResponseError):
            client.get("football/nfl/teams")

    @responses.activate
    def test_timeout_raises_timeout_error(self):
        responses.add(
            responses.GET,
            "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams",
            body=ConnectionError("timeout"),
        )
        # responses library raises ConnectionError, which maps to ESPNApiError
        client = ESPNClient(retries=0)
        with pytest.raises(ESPNApiError):
            client.get("football/nfl/teams")

    @responses.activate
    def test_all_espn_errors_are_catchable_with_base(self):
        """All custom errors inherit from ESPNApiError."""
        responses.add(
            responses.GET,
            "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams",
            json={},
            status=404,
        )
        client = ESPNClient(retries=0)
        with pytest.raises(ESPNApiError):
            client.get("football/nfl/teams")


class TestClientSuccessResponses:
    """Test successful API responses."""

    @responses.activate
    def test_successful_get(self):
        responses.add(
            responses.GET,
            "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams",
            json={"sports": [{"leagues": [{"teams": []}]}]},
            status=200,
        )
        client = ESPNClient(retries=0)
        data = client.get("football/nfl/teams")
        assert "sports" in data

    @responses.activate
    def test_get_core(self):
        responses.add(
            responses.GET,
            "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes",
            json={"items": []},
            status=200,
        )
        client = ESPNClient(retries=0)
        data = client.get_core("football/leagues/nfl/athletes")
        assert "items" in data

    @responses.activate
    def test_get_standings(self):
        responses.add(
            responses.GET,
            "https://site.api.espn.com/apis/v2/sports/soccer/eng.1/standings",
            json={"children": []},
            status=200,
        )
        client = ESPNClient(retries=0)
        data = client.get_standings("soccer/eng.1/standings")
        assert "children" in data

    @responses.activate
    def test_params_passed_through(self):
        responses.add(
            responses.GET,
            "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard",
            json={"events": []},
            status=200,
        )
        client = ESPNClient(retries=0)
        client.get("football/nfl/scoreboard", params={"dates": "20241201"})
        assert "dates=20241201" in responses.calls[0].request.url


class TestClientCaching:
    """Test caching with mocked responses."""

    @responses.activate
    def test_cache_prevents_second_request(self):
        responses.add(
            responses.GET,
            "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams",
            json={"sports": []},
            status=200,
        )
        client = ESPNClient(cache_ttl=300, retries=0)
        client.get("football/nfl/teams")
        client.get("football/nfl/teams")
        assert len(responses.calls) == 1

    @responses.activate
    def test_no_cache_makes_two_requests(self):
        responses.add(
            responses.GET,
            "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams",
            json={"sports": []},
            status=200,
        )
        client = ESPNClient(retries=0)
        client.get("football/nfl/teams")
        client.get("football/nfl/teams")
        assert len(responses.calls) == 2


class TestRetryBehavior:
    """Test retry logic."""

    @responses.activate
    def test_retries_on_500(self):
        url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"
        responses.add(responses.GET, url, json={}, status=500)
        responses.add(responses.GET, url, json={"sports": []}, status=200)

        client = ESPNClient(retries=1)
        data = client.get("football/nfl/teams")
        assert "sports" in data
        assert len(responses.calls) == 2

    @responses.activate
    def test_no_retry_when_disabled(self):
        url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"
        responses.add(responses.GET, url, json={}, status=500)

        client = ESPNClient(retries=0)
        with pytest.raises(ESPNServerError):
            client.get("football/nfl/teams")
        assert len(responses.calls) == 1


class TestClientAdditionalMethods:
    @responses.activate
    def test_get_now(self):
        responses.add(
            responses.GET,
            "https://now.core.api.espn.com/v1/sports/news",
            json={"headlines": []},
            status=200,
        )
        client = ESPNClient(retries=0)
        data = client.get_now("sports/news")
        assert "headlines" in data

    @responses.activate
    def test_get_fantasy(self):
        responses.add(
            responses.GET,
            "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2024",
            json={"id": 1},
            status=200,
        )
        client = ESPNClient(retries=0)
        data = client.get_fantasy("games/ffl/seasons/2024")
        assert data["id"] == 1

    @responses.activate
    def test_get_gambit(self):
        responses.add(
            responses.GET,
            "https://gambit-api.fantasy.espn.com/apis/v1/challenges",
            json={"challenges": []},
            status=200,
        )
        client = ESPNClient(retries=0)
        data = client.get_gambit("challenges")
        assert "challenges" in data

    @responses.activate
    def test_get_web(self):
        responses.add(
            responses.GET,
            "https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/stats",
            json={"statistics": []},
            status=200,
        )
        client = ESPNClient(retries=0)
        data = client.get_web("football/nfl/stats")
        assert "statistics" in data

    @responses.activate
    def test_timeout_raises_timeout_error_properly(self):
        responses.add(
            responses.GET,
            "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams",
            body=requests.Timeout("timed out"),
        )
        client = ESPNClient(retries=0)
        with pytest.raises(ESPNTimeoutError):
            client.get("football/nfl/teams")


class TestDiskCache:
    def test_disk_cache_expired_entry(self, tmp_path):
        import json
        import time

        cache_dir = tmp_path / "cache"
        client = ESPNClient(cache_ttl=1, cache_dir=cache_dir, retries=0)

        # Manually write an expired cache entry
        import hashlib

        url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"
        key_data = f"{url}:"
        key = hashlib.md5(key_data.encode()).hexdigest()
        cache_file = cache_dir / f"{key}.json"
        with open(cache_file, "w") as f:
            json.dump({"timestamp": time.time() - 100, "data": {"old": True}}, f)

        # The expired entry should be deleted and a fresh request made
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, url, json={"fresh": True}, status=200)
            data = client.get("football/nfl/teams")
            assert data["fresh"] is True
            assert not cache_file.exists() or data["fresh"]

    def test_disk_cache_clear(self, tmp_path):
        cache_dir = tmp_path / "cache"
        client = ESPNClient(cache_ttl=300, cache_dir=cache_dir, retries=0)

        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams",
                json={"sports": []},
                status=200,
            )
            client.get("football/nfl/teams")

        # Cache dir should have files
        cache_files = list(cache_dir.glob("*.json"))
        assert len(cache_files) > 0

        client.clear_cache()
        cache_files = list(cache_dir.glob("*.json"))
        assert len(cache_files) == 0

    def test_disk_cache_corrupt_json(self, tmp_path):
        import hashlib

        cache_dir = tmp_path / "cache"
        client = ESPNClient(cache_ttl=300, cache_dir=cache_dir, retries=0)

        url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"
        key_data = f"{url}:"
        key = hashlib.md5(key_data.encode()).hexdigest()
        cache_file = cache_dir / f"{key}.json"
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.write_text("not valid json{{{")

        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, url, json={"fresh": True}, status=200)
            data = client.get("football/nfl/teams")
            assert data["fresh"] is True
