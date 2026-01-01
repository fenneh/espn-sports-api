"""Tests for data models module."""

from espn_sports_api.models import (
    Athlete,
    Broadcast,
    Injury,
    Team,
    Transaction,
    Venue,
    Weather,
    parse_injuries,
    parse_teams,
)


class TestVenue:
    """Tests for Venue model."""

    def test_from_dict(self):
        """Test creating Venue from dict."""
        data = {
            "id": "1",
            "fullName": "Arrowhead Stadium",
            "address": {
                "city": "Kansas City",
                "state": "MO",
                "country": "USA",
            },
            "capacity": 76416,
            "indoor": False,
            "grass": True,
        }
        venue = Venue.from_dict(data)

        assert venue.id == "1"
        assert venue.name == "Arrowhead Stadium"
        assert venue.city == "Kansas City"
        assert venue.state == "MO"
        assert venue.capacity == 76416
        assert venue.indoor is False
        assert venue.grass is True

    def test_from_dict_minimal(self):
        """Test creating Venue with minimal data."""
        data = {"id": "1", "name": "Stadium"}
        venue = Venue.from_dict(data)

        assert venue.id == "1"
        assert venue.name == "Stadium"
        assert venue.capacity is None


class TestBroadcast:
    """Tests for Broadcast model."""

    def test_from_dict(self):
        """Test creating Broadcast from dict."""
        data = {
            "names": ["ESPN"],
            "market": "National",
            "lang": "en",
            "region": "US",
        }
        broadcast = Broadcast.from_dict(data)

        assert broadcast.network == "ESPN"
        assert broadcast.market == "National"
        assert broadcast.language == "en"


class TestWeather:
    """Tests for Weather model."""

    def test_from_dict(self):
        """Test creating Weather from dict."""
        data = {
            "temperature": 72,
            "displayValue": "Partly Cloudy",
            "highTemperature": 78,
            "lowTemperature": 65,
        }
        weather = Weather.from_dict(data)

        assert weather.temperature == 72
        assert weather.conditions == "Partly Cloudy"
        assert weather.high_temp == 78
        assert weather.low_temp == 65


class TestInjury:
    """Tests for Injury model."""

    def test_from_dict(self, sample_injury_response):
        """Test creating Injury from dict."""
        data = sample_injury_response["items"][0]
        injury = Injury.from_dict(data)

        assert injury.athlete_id == "12345"
        assert injury.athlete_name == "John Doe"
        assert injury.status == "Questionable"
        assert injury.injury_type == "Ankle"
        assert injury.body_part == "Leg"
        assert injury.return_date == "2024-01-15"


class TestTransaction:
    """Tests for Transaction model."""

    def test_from_dict(self):
        """Test creating Transaction from dict."""
        data = {
            "id": "1",
            "date": "2024-01-15",
            "type": {"text": "Signed"},
            "description": "Signed to practice squad",
            "team": {"displayName": "Team A"},
            "athlete": {"displayName": "John Doe"},
        }
        txn = Transaction.from_dict(data)

        assert txn.id == "1"
        assert txn.transaction_type == "Signed"
        assert txn.athlete_name == "John Doe"


class TestAthlete:
    """Tests for Athlete model."""

    def test_from_dict(self):
        """Test creating Athlete from dict."""
        data = {
            "id": "12345",
            "displayName": "John Doe",
            "firstName": "John",
            "lastName": "Doe",
            "jersey": "12",
            "position": {"abbreviation": "QB"},
            "team": {"displayName": "Team A"},
            "displayHeight": "6-4",
            "weight": 220,
            "age": 28,
            "college": {"name": "State University"},
            "birthPlace": {"city": "New York", "state": "NY"},
            "experience": {"years": 6},
            "headshot": {"href": "https://example.com/photo.png"},
        }
        athlete = Athlete.from_dict(data)

        assert athlete.id == "12345"
        assert athlete.name == "John Doe"
        assert athlete.jersey == "12"
        assert athlete.position == "QB"
        assert athlete.height == "6-4"
        assert athlete.weight == 220
        assert athlete.age == 28
        assert athlete.experience == 6


class TestTeam:
    """Tests for Team model."""

    def test_from_dict(self, sample_team_response):
        """Test creating Team from dict."""
        team_data = sample_team_response["sports"][0]["leagues"][0]["teams"][0]["team"]
        team = Team.from_dict(team_data)

        assert team.id == "1"
        assert team.name == "New England Patriots"
        assert team.abbreviation == "NE"
        assert team.nickname == "Patriots"
        assert team.color == "002244"


class TestParsingHelpers:
    """Tests for parsing helper functions."""

    def test_parse_injuries(self, sample_injury_response):
        """Test parse_injuries function."""
        injuries = parse_injuries(sample_injury_response)

        assert len(injuries) == 1
        assert injuries[0].athlete_name == "John Doe"

    def test_parse_teams(self, sample_team_response):
        """Test parse_teams function."""
        teams = parse_teams(sample_team_response)

        assert len(teams) == 1
        assert teams[0].name == "New England Patriots"

    def test_parse_injuries_empty(self):
        """Test parsing empty injuries response."""
        injuries = parse_injuries({"items": []})
        assert injuries == []

    def test_parse_teams_empty(self):
        """Test parsing empty teams response."""
        teams = parse_teams({"sports": []})
        assert teams == []
