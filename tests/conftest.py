"""Pytest fixtures for ESPN API tests."""

import pytest

from espn_sports_api import (
    MLB,
    NBA,
    NCAAB,
    NCAAF,
    NFL,
    NHL,
    UFC,
    ESPNClient,
    Golf,
    Racing,
    Soccer,
    Tennis,
)


@pytest.fixture
def client():
    """Create ESPN client."""
    return ESPNClient()


@pytest.fixture
def nfl():
    """Create NFL instance."""
    return NFL()


@pytest.fixture
def nba():
    """Create NBA instance."""
    return NBA()


@pytest.fixture
def mlb():
    """Create MLB instance."""
    return MLB()


@pytest.fixture
def nhl():
    """Create NHL instance."""
    return NHL()


@pytest.fixture
def soccer():
    """Create Soccer instance (EPL)."""
    return Soccer(league="epl")


@pytest.fixture
def ufc():
    """Create UFC instance."""
    return UFC()


@pytest.fixture
def golf():
    """Create Golf instance."""
    return Golf()


@pytest.fixture
def racing():
    """Create Racing instance (F1)."""
    return Racing(series="f1")


@pytest.fixture
def tennis():
    """Create Tennis instance."""
    return Tennis()


@pytest.fixture
def ncaaf():
    """Create NCAAF instance."""
    return NCAAF()


@pytest.fixture
def ncaab():
    """Create NCAAB instance."""
    return NCAAB()


# Sample API responses for unit tests
@pytest.fixture
def sample_scoreboard_response():
    """Sample scoreboard response with odds."""
    return {
        "events": [
            {
                "id": "401547417",
                "name": "Team A at Team B",
                "competitions": [
                    {
                        "id": "401547417",
                        "competitors": [
                            {
                                "homeAway": "home",
                                "team": {"displayName": "Team B"},
                                "score": "24",
                            },
                            {
                                "homeAway": "away",
                                "team": {"displayName": "Team A"},
                                "score": "17",
                            },
                        ],
                        "odds": [
                            {
                                "provider": {"name": "DraftKings"},
                                "details": "Team B -3.5",
                                "spread": -3.5,
                                "overUnder": 45.5,
                                "pointSpread": {
                                    "american": {
                                        "favorite": {"close": -110},
                                        "underdog": {"close": -110},
                                    }
                                },
                                "moneyline": {
                                    "home": {"close": -150},
                                    "away": {"close": 130},
                                },
                                "total": {
                                    "over": {"close": -110},
                                    "under": {"close": -110},
                                },
                            }
                        ],
                    }
                ],
            }
        ]
    }


@pytest.fixture
def sample_injury_response():
    """Sample injury API response."""
    return {
        "items": [
            {
                "athlete": {
                    "id": "12345",
                    "displayName": "John Doe",
                    "team": {"displayName": "Team A"},
                    "position": {"abbreviation": "QB"},
                },
                "status": "Questionable",
                "details": {
                    "type": "Ankle",
                    "location": "Leg",
                    "returnDate": "2024-01-15",
                },
                "longComment": "Day-to-day with ankle sprain",
            }
        ]
    }


@pytest.fixture
def sample_team_response():
    """Sample teams API response."""
    return {
        "sports": [
            {
                "leagues": [
                    {
                        "teams": [
                            {
                                "team": {
                                    "id": "1",
                                    "displayName": "New England Patriots",
                                    "abbreviation": "NE",
                                    "location": "New England",
                                    "nickname": "Patriots",
                                    "color": "002244",
                                    "alternateColor": "c60c30",
                                    "logos": [{"href": "https://example.com/logo.png"}],
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }
