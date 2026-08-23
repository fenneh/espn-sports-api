"""Tests for caching functionality."""

import time

import responses

from espn_sports_api import Cache, ESPNClient


class TestCache:
    """Tests for Cache class."""

    def test_cache_init_memory_only(self):
        """Test cache initialization without disk storage."""
        cache = Cache(ttl=60)
        assert cache.ttl == 60
        assert cache.cache_dir is None

    def test_cache_init_with_disk(self, tmp_path):
        """Test cache initialization with disk storage."""
        cache = Cache(ttl=60, cache_dir=tmp_path / "cache")
        assert cache.cache_dir is not None
        assert cache.cache_dir.exists()

    def test_cache_set_and_get(self):
        """Test setting and getting cached data."""
        cache = Cache(ttl=60)
        cache.set("http://example.com/api", {"foo": "bar"}, {"result": 123})

        result = cache.get("http://example.com/api", {"foo": "bar"})
        assert result == {"result": 123}

    def test_cache_miss(self):
        """Test cache miss returns None."""
        cache = Cache(ttl=60)
        result = cache.get("http://example.com/nonexistent", None)
        assert result is None

    def test_cache_expiry(self):
        """Test cache entry expires after TTL."""
        cache = Cache(ttl=1)  # 1 second TTL
        cache.set("http://example.com/api", None, {"result": 123})

        # Should be cached
        assert cache.get("http://example.com/api", None) == {"result": 123}

        # Wait for expiry
        time.sleep(1.1)
        assert cache.get("http://example.com/api", None) is None

    def test_cache_clear(self):
        """Test clearing cache."""
        cache = Cache(ttl=60)
        cache.set("http://example.com/api1", None, {"result": 1})
        cache.set("http://example.com/api2", None, {"result": 2})

        cache.clear()

        assert cache.get("http://example.com/api1", None) is None
        assert cache.get("http://example.com/api2", None) is None

    def test_cache_disk_persistence(self, tmp_path):
        """Test cache persists to disk and can be read back."""
        cache_dir = tmp_path / "cache"
        cache1 = Cache(ttl=60, cache_dir=cache_dir)
        cache1.set("http://example.com/api", None, {"result": 123})

        # Create new cache instance pointing to same directory
        cache2 = Cache(ttl=60, cache_dir=cache_dir)

        # Should find the cached data
        result = cache2.get("http://example.com/api", None)
        assert result == {"result": 123}

    def test_cache_key_generation(self):
        """Test different params generate different keys."""
        cache = Cache(ttl=60)
        cache.set("http://example.com/api", {"a": 1}, {"result": "a1"})
        cache.set("http://example.com/api", {"a": 2}, {"result": "a2"})

        assert cache.get("http://example.com/api", {"a": 1}) == {"result": "a1"}
        assert cache.get("http://example.com/api", {"a": 2}) == {"result": "a2"}


class TestESPNClientCaching:
    """Tests for ESPNClient caching."""

    def test_client_no_cache_by_default(self):
        """Test client has no cache by default."""
        client = ESPNClient()
        assert client._cache is None

    def test_client_with_cache(self):
        """Test client can be initialized with cache."""
        client = ESPNClient(cache_ttl=300)
        assert client._cache is not None
        assert client._cache.ttl == 300

    def test_client_with_disk_cache(self, tmp_path):
        """Test client with disk cache."""
        cache_dir = tmp_path / "cache"
        client = ESPNClient(cache_ttl=300, cache_dir=cache_dir)
        assert client._cache is not None
        assert client._cache.cache_dir == cache_dir
        assert cache_dir.exists()

    def test_client_clear_cache(self):
        """Test clearing client cache."""
        client = ESPNClient(cache_ttl=300)
        assert client._cache is not None

        client._cache.set("http://test.com", None, {"test": 1})
        assert client._cache.get("http://test.com", None) is not None

        client.clear_cache()
        assert client._cache.get("http://test.com", None) is None

    def test_client_clear_cache_no_cache(self):
        """Test clear_cache doesn't error when cache not enabled."""
        client = ESPNClient()
        client.clear_cache()  # Should not raise


class TestCachingIntegration:
    """Integration tests for caching, with the HTTP layer mocked."""

    @responses.activate
    def test_cached_request_skips_second_http_call(self):
        """Test that a cached request doesn't hit the API again."""
        responses.add(
            responses.GET,
            "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams",
            json={"teams": []},
            status=200,
        )
        client = ESPNClient(cache_ttl=60)

        response1 = client.get("football/nfl/teams")
        response2 = client.get("football/nfl/teams")

        assert response1 == response2
        assert len(responses.calls) == 1

        client.close()

    @responses.activate
    def test_different_params_not_cached(self):
        """Test that different params create separate cache entries."""
        responses.add(
            responses.GET,
            "https://site.api.espn.com/apis/site/v2/sports/football/nfl/news",
            json={"articles": [1]},
            status=200,
        )
        responses.add(
            responses.GET,
            "https://site.api.espn.com/apis/site/v2/sports/football/nfl/news",
            json={"articles": [1, 2]},
            status=200,
        )
        client = ESPNClient(cache_ttl=60)

        response1 = client.get("football/nfl/news", {"limit": 1})
        response2 = client.get("football/nfl/news", {"limit": 2})

        assert response1["articles"] == [1]
        assert response2["articles"] == [1, 2]
        assert len(responses.calls) == 2

        client.close()
