"""Tests for odds extraction module."""

from espn_sports_api.odds import GameOdds, Moneyline, Odds, Spread, Total


class TestOddsDataclasses:
    """Test odds dataclasses."""

    def test_spread_dataclass(self):
        """Test Spread dataclass creation."""
        spread = Spread(
            favorite="Team A",
            spread=3.5,
            favorite_odds=-110,
            underdog_odds=-110,
            provider="DraftKings",
        )
        assert spread.favorite == "Team A"
        assert spread.spread == 3.5

    def test_moneyline_dataclass(self):
        """Test Moneyline dataclass creation."""
        ml = Moneyline(
            home_team="Team A",
            away_team="Team B",
            home_odds=-150,
            away_odds=130,
            provider="DraftKings",
        )
        assert ml.home_odds == -150
        assert ml.away_odds == 130

    def test_total_dataclass(self):
        """Test Total dataclass creation."""
        total = Total(
            over_under=45.5,
            over_odds=-110,
            under_odds=-110,
            provider="DraftKings",
        )
        assert total.over_under == 45.5

    def test_game_odds_dataclass(self):
        """Test GameOdds dataclass creation."""
        odds = GameOdds(
            event_id="123",
            home_team="Team A",
            away_team="Team B",
        )
        assert odds.event_id == "123"
        assert odds.spread is None
        assert odds.moneyline is None
        assert odds.total is None


class TestOddsExtraction:
    """Test odds extraction from API responses."""

    def test_from_event(self, sample_scoreboard_response):
        """Test extracting odds from single event."""
        event = sample_scoreboard_response["events"][0]
        odds = Odds.from_event(event)

        assert odds is not None
        assert odds.event_id == "401547417"
        assert odds.home_team == "Team B"
        assert odds.away_team == "Team A"

    def test_from_event_with_spread(self, sample_scoreboard_response):
        """Test spread extraction."""
        event = sample_scoreboard_response["events"][0]
        odds = Odds.from_event(event)

        assert odds.spread is not None
        assert odds.spread.spread == 3.5
        assert odds.spread.provider == "DraftKings"

    def test_from_event_with_moneyline(self, sample_scoreboard_response):
        """Test moneyline extraction."""
        event = sample_scoreboard_response["events"][0]
        odds = Odds.from_event(event)

        assert odds.moneyline is not None
        assert odds.moneyline.home_odds == -150
        assert odds.moneyline.away_odds == 130

    def test_from_event_with_total(self, sample_scoreboard_response):
        """Test over/under extraction."""
        event = sample_scoreboard_response["events"][0]
        odds = Odds.from_event(event)

        assert odds.total is not None
        assert odds.total.over_under == 45.5

    def test_from_scoreboard(self, sample_scoreboard_response):
        """Test extracting all odds from scoreboard."""
        all_odds = Odds.from_scoreboard(sample_scoreboard_response)

        assert len(all_odds) == 1
        assert all_odds[0].event_id == "401547417"

    def test_spreads_helper(self, sample_scoreboard_response):
        """Test spreads helper method."""
        spreads = Odds.spreads(sample_scoreboard_response)

        assert len(spreads) == 1
        assert spreads[0]["spread"] == 3.5
        assert spreads[0]["home"] == "Team B"

    def test_moneylines_helper(self, sample_scoreboard_response):
        """Test moneylines helper method."""
        moneylines = Odds.moneylines(sample_scoreboard_response)

        assert len(moneylines) == 1
        assert moneylines[0]["home_odds"] == -150

    def test_totals_helper(self, sample_scoreboard_response):
        """Test totals helper method."""
        totals = Odds.totals(sample_scoreboard_response)

        assert len(totals) == 1
        assert totals[0]["over_under"] == 45.5

    def test_from_event_no_odds(self):
        """Test extraction when no odds present."""
        event = {
            "id": "123",
            "competitions": [
                {
                    "competitors": [
                        {"homeAway": "home", "team": {"displayName": "A"}},
                        {"homeAway": "away", "team": {"displayName": "B"}},
                    ]
                }
            ],
        }
        odds = Odds.from_event(event)
        assert odds is None

    def test_from_event_no_competitions(self):
        """Test extraction when no competitions."""
        event = {"id": "123"}
        odds = Odds.from_event(event)
        assert odds is None

    def test_empty_scoreboard(self):
        """Test extraction from empty scoreboard."""
        all_odds = Odds.from_scoreboard({"events": []})
        assert all_odds == []
