"""Tests for data models module."""

from espn_sports_api.models import (
    Athlete,
    Broadcast,
    Injury,
    Team,
    Transaction,
    Venue,
    Weather,
    parse_athletes,
    parse_injuries,
    parse_teams,
    parse_transactions,
    parse_venues,
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

    def test_parse_transactions(self):
        txns = parse_transactions(
            {
                "items": [
                    {
                        "id": "1",
                        "date": "2024-01-15",
                        "type": {"text": "Signed"},
                        "description": "Signed player",
                        "team": {"displayName": "Team A"},
                    }
                ]
            }
        )
        assert len(txns) == 1
        assert txns[0].transaction_type == "Signed"

    def test_parse_transactions_fallback_key(self):
        txns = parse_transactions(
            {
                "transactions": [
                    {
                        "id": "2",
                        "date": "2024-02-01",
                        "type": {"text": "Trade"},
                        "description": "Traded",
                        "team": {"displayName": "Team B"},
                    }
                ]
            }
        )
        assert len(txns) == 1
        assert txns[0].transaction_type == "Trade"

    def test_parse_transactions_empty(self):
        assert parse_transactions({"items": []}) == []

    def test_parse_venues(self):
        venues = parse_venues(
            {
                "items": [
                    {
                        "id": "1",
                        "fullName": "Test Stadium",
                        "address": {"city": "Boston", "state": "MA", "country": "USA"},
                        "capacity": 50000,
                    }
                ]
            }
        )
        assert len(venues) == 1
        assert venues[0].name == "Test Stadium"

    def test_parse_venues_fallback_key(self):
        venues = parse_venues(
            {
                "venues": [
                    {
                        "id": "2",
                        "name": "Arena",
                        "address": {"city": "LA", "state": "CA", "country": "USA"},
                    }
                ]
            }
        )
        assert len(venues) == 1
        assert venues[0].name == "Arena"

    def test_parse_venues_empty(self):
        assert parse_venues({"items": []}) == []

    def test_parse_athletes(self):
        athletes = parse_athletes(
            {
                "items": [
                    {
                        "id": "1",
                        "displayName": "Test Player",
                        "firstName": "Test",
                        "lastName": "Player",
                    }
                ]
            }
        )
        assert len(athletes) == 1
        assert athletes[0].name == "Test Player"

    def test_parse_athletes_fallback_key(self):
        athletes = parse_athletes(
            {
                "athletes": [
                    {
                        "id": "2",
                        "displayName": "Other Player",
                        "firstName": "Other",
                        "lastName": "Player",
                    }
                ]
            }
        )
        assert len(athletes) == 1

    def test_parse_athletes_empty(self):
        assert parse_athletes({"items": []}) == []

    def test_parse_injuries_nested_structure(self):
        injuries = parse_injuries(
            {
                "injuries": [
                    {
                        "displayName": "Kansas City Chiefs",
                        "injuries": [
                            {
                                "athlete": {
                                    "id": "99",
                                    "displayName": "Injured Guy",
                                    "position": {"abbreviation": "WR"},
                                },
                                "status": "Out",
                                "details": {"type": "Knee", "location": "Leg"},
                                "shortComment": "Torn ACL",
                            }
                        ],
                    }
                ]
            }
        )
        assert len(injuries) == 1
        assert injuries[0].athlete_name == "Injured Guy"
        assert injuries[0].team == "Kansas City Chiefs"


class TestModelStr:
    def test_venue_str(self):
        v = Venue(id="1", name="Arrowhead", city="KC", state="MO", country="USA", capacity=76416)
        assert "Arrowhead" in str(v)
        assert "KC, MO" in str(v)
        assert "76,416" in str(v)

    def test_venue_str_no_state(self):
        v = Venue(id="1", name="Wembley", city="London", state="", country="UK")
        assert "London" in str(v)

    def test_venue_str_no_capacity(self):
        v = Venue(id="1", name="Test", city="X", state="Y", country="Z")
        assert "capacity" not in str(v)

    def test_broadcast_str(self):
        b = Broadcast(network="ESPN", market="National", language="en", region="US")
        assert str(b) == "ESPN"

    def test_weather_str(self):
        w = Weather(temperature=72, conditions="Sunny")
        assert str(w) == "72°F, Sunny"

    def test_injury_str(self):
        i = Injury(
            athlete_id="1",
            athlete_name="John Doe",
            team="Team A",
            position="QB",
            status="Questionable",
            injury_type="Ankle",
            body_part="Leg",
            description="Day to day",
        )
        s = str(i)
        assert "John Doe" in s
        assert "QB" in s
        assert "Team A" in s
        assert "Questionable" in s

    def test_injury_str_no_type_uses_body_part(self):
        i = Injury(
            athlete_id="1",
            athlete_name="Jane",
            team="T",
            position="C",
            status="Out",
            injury_type="",
            body_part="Knee",
            description="",
        )
        assert "Knee" in str(i)

    def test_transaction_str(self):
        t = Transaction(
            id="1",
            date="2024-01-15",
            transaction_type="Signed",
            description="Signed",
            team="Team A",
            athlete_name="John Doe",
        )
        s = str(t)
        assert "John Doe" in s
        assert "Team A" in s
        assert "2024-01-15" in s

    def test_transaction_str_no_athlete(self):
        t = Transaction(
            id="1",
            date="2024-01-15",
            transaction_type="Trade",
            description="Multi-player trade",
            team="Team B",
        )
        assert "Team B" in str(t)

    def test_athlete_str(self):
        a = Athlete(
            id="1",
            name="John Doe",
            first_name="John",
            last_name="Doe",
            jersey="12",
            position="QB",
            team="Team A",
        )
        s = str(a)
        assert "#12" in s
        assert "John Doe" in s
        assert "QB" in s
        assert "Team A" in s

    def test_athlete_str_minimal(self):
        a = Athlete(id="1", name="Jane Doe", first_name="Jane", last_name="Doe")
        assert str(a) == "Jane Doe"

    def test_team_str(self):
        t = Team(
            id="1",
            name="New England Patriots",
            abbreviation="NE",
            location="New England",
            nickname="Patriots",
            color="002244",
            alternate_color="c60c30",
            record="10-7",
        )
        s = str(t)
        assert "New England Patriots" in s
        assert "NE" in s
        assert "10-7" in s

    def test_team_str_no_record(self):
        t = Team(
            id="1",
            name="Test Team",
            abbreviation="TT",
            location="Test",
            nickname="Testers",
            color="000000",
            alternate_color="ffffff",
        )
        s = str(t)
        assert "Test Team (TT)" == s


class TestTeamFromDictWithRecord:
    def test_team_with_record(self):
        data = {
            "id": "10",
            "displayName": "Test Team",
            "abbreviation": "TT",
            "location": "Test",
            "nickname": "Testers",
            "color": "000",
            "alternateColor": "fff",
            "logos": [],
            "record": {"items": [{"summary": "10-7"}]},
        }
        team = Team.from_dict(data)
        assert team.record == "10-7"


class TestExceptionInstantiation:
    def test_timeout_error_default(self):
        from espn_sports_api.exceptions import ESPNTimeoutError

        e = ESPNTimeoutError()
        assert e.status_code is None
        assert "timed out" in str(e).lower()


class TestAthleteOptionalDefaults:
    def test_from_dict_minimal(self):
        data = {
            "id": "999",
            "displayName": "Minimal Player",
            "firstName": "Min",
            "lastName": "Player",
        }
        a = Athlete.from_dict(data)
        assert a.id == "999"
        assert a.name == "Minimal Player"
        assert a.jersey is None
        assert a.position is None
        assert a.team is None
        assert a.height is None
        assert a.weight is None
        assert a.age is None
        assert a.college is None
        assert a.birthplace is None
        assert a.experience is None
        assert a.headshot_url is None
