from datetime import date

import pytest
import responses
from responses import matchers

from espn_sports_api import ESPNApiError, ESPNClient, ESPNResponseError, Soccer

PRIMARY = "https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard"
CDN = "https://cdn.espn.com/core/soccer/scoreboard"


def block_primary(status=403):
    responses.get(PRIMARY, status=status)


def add_scoreboard(day, data):
    responses.get(
        CDN,
        json={"content": {"sbData": data}},
        match=[matchers.query_param_matcher({"xhr": "1", "league": "eng.1", "date": day})],
    )


@responses.activate
def test_on_date_preserves_fixture_and_goal_data():
    block_primary()
    event = {
        "id": "123",
        "date": "20261010T11:30Z",
        "status": {"type": {"name": "STATUS_FIRST_HALF", "state": "in"}},
        "competitions": [
            {
                "competitors": [
                    {"homeAway": "home", "team": {"id": "359"}, "score": "1"},
                    {"homeAway": "away", "team": {"id": "357"}, "score": "0"},
                ],
                "details": [{"type": {"text": "Goal"}, "team": {"id": "359"}}],
            }
        ],
    }
    data = {"events": [event], "leagues": [{"slug": "eng.1"}]}
    add_scoreboard("20261010", data)

    assert Soccer().on_date(date(2026, 10, 10)) == data
    assert len(responses.calls) == 2


@responses.activate
def test_successful_primary_does_not_use_cdn():
    responses.get(PRIMARY, json={"events": []})
    assert Soccer().on_date("20261010") == {"events": []}
    assert len(responses.calls) == 1


@responses.activate
def test_empty_match_day_is_valid():
    block_primary()
    add_scoreboard("20260928", {"events": []})
    assert Soccer().on_date("20260928") == {"events": []}


@responses.activate
def test_date_range_includes_every_day():
    block_primary()
    add_scoreboard("20261010", {"events": [{"id": "1"}]})
    add_scoreboard("20261011", {"events": [{"id": "2"}]})
    data = Soccer().date_range("20261010", "20261011")
    assert data["events"] == [{"id": "1"}, {"id": "2"}]


@responses.activate
def test_scoreboard_range_does_not_lose_date_filter():
    block_primary()
    add_scoreboard("20261010", {"events": [{"id": "1"}]})
    add_scoreboard("20261011", {"events": [{"id": "2"}]})
    data = Soccer().scoreboard(dates="20261010-20261011")
    assert data["events"] == [{"id": "1"}, {"id": "2"}]


@responses.activate
def test_fallback_uses_existing_cache():
    block_primary()
    add_scoreboard("20261010", {"events": [{"id": "1"}]})
    soccer = Soccer(client=ESPNClient(cache_ttl=60))
    assert soccer.on_date("20261010") == soccer.on_date("20261010")
    assert len(responses.calls) == 2


@pytest.mark.parametrize(
    "payload", [{}, {"content": {"sbData": {}}}, {"content": {"sbData": {"events": None}}}]
)
@responses.activate
def test_invalid_fallback_response_raises(payload):
    block_primary()
    responses.get(CDN, json=payload)
    with pytest.raises(ESPNResponseError):
        Soccer().on_date("20261010")


@responses.activate
def test_failed_fallback_is_not_cached():
    block_primary()
    responses.get(CDN, status=503)
    add_scoreboard("20261010", {"events": [{"id": "1"}]})
    soccer = Soccer(client=ESPNClient(cache_ttl=60, retries=0))
    with pytest.raises(ESPNApiError) as error:
        soccer.on_date("20261010")
    assert error.value.status_code == 503
    assert soccer.on_date("20261010")["events"] == [{"id": "1"}]


@responses.activate
def test_other_primary_errors_are_not_retried_on_cdn():
    block_primary(status=404)
    with pytest.raises(ESPNApiError) as error:
        Soccer().on_date("20261010")
    assert error.value.status_code == 404
    assert len(responses.calls) == 1
