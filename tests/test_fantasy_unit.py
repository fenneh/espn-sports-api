"""Unit tests for fantasy endpoints with mocked HTTP responses.

Each test verifies the correct URL, query params, and data passthrough.
"""

import responses

from espn_sports_api import FantasyFootball

FANTASY = "https://lm-api-reads.fantasy.espn.com/apis/v3"


class TestFantasyLeagueMethods:
    def _league(self):
        return FantasyFootball(league_id=123456, season=2024)

    def _url(self):
        return f"{FANTASY}/games/ffl/seasons/2024/segments/0/leagues/123456"

    @responses.activate
    def test_info_hits_base_league_endpoint(self):
        responses.add(responses.GET, self._url(), json={"id": 123456, "name": "My League"})
        data = self._league().info()
        assert data["id"] == 123456
        assert data["name"] == "My League"
        assert "view" not in (responses.calls[0].request.url or "")

    @responses.activate
    def test_teams_passes_mteam_view(self):
        responses.add(responses.GET, self._url(), json={"teams": [{"id": 1}]})
        data = self._league().teams()
        assert data["teams"][0]["id"] == 1
        assert "view=mTeam" in responses.calls[0].request.url

    @responses.activate
    def test_roster_passes_view_and_team_id(self):
        responses.add(responses.GET, self._url(), json={"teams": [{"roster": {"entries": []}}]})
        data = self._league().roster(team_id=1)
        assert "roster" in data["teams"][0]
        url = responses.calls[0].request.url
        assert "view=mRoster" in url
        assert "forTeamId=1" in url

    @responses.activate
    def test_matchups_passes_mmatchup_view(self):
        responses.add(responses.GET, self._url(), json={"schedule": [{"matchupPeriodId": 1}]})
        data = self._league().matchups()
        assert data["schedule"][0]["matchupPeriodId"] == 1
        url = responses.calls[0].request.url
        assert "view=mMatchup" in url
        assert "scoringPeriodId" not in url

    @responses.activate
    def test_matchups_passes_scoring_period_when_week_given(self):
        responses.add(responses.GET, self._url(), json={"schedule": []})
        self._league().matchups(week=5)
        url = responses.calls[0].request.url
        assert "scoringPeriodId=5" in url
        assert "view=mMatchup" in url

    @responses.activate
    def test_standings_passes_mstandings_view(self):
        responses.add(responses.GET, self._url(), json={"teams": [{"record": {"wins": 10}}]})
        data = self._league().standings()
        assert data["teams"][0]["record"]["wins"] == 10
        assert "view=mStandings" in responses.calls[0].request.url

    @responses.activate
    def test_free_agents_passes_kona_view(self):
        responses.add(responses.GET, self._url(), json={"players": [{"fullName": "Player X"}]})
        data = self._league().free_agents()
        assert data["players"][0]["fullName"] == "Player X"
        url = responses.calls[0].request.url
        assert "view=kona_player_info" in url
        assert "filterSlotIds" not in url

    @responses.activate
    def test_free_agents_passes_position_filter(self):
        responses.add(responses.GET, self._url(), json={"players": []})
        self._league().free_agents(position="QB")
        url = responses.calls[0].request.url
        assert "filterSlotIds=QB" in url
        assert "view=kona_player_info" in url

    @responses.activate
    def test_draft_passes_mdraftdetail_view(self):
        responses.add(
            responses.GET,
            self._url(),
            json={"draftDetail": {"drafted": True, "picks": []}},
        )
        data = self._league().draft()
        assert data["draftDetail"]["drafted"] is True
        assert "view=mDraftDetail" in responses.calls[0].request.url

    @responses.activate
    def test_transactions_passes_mtransactions2_view(self):
        responses.add(
            responses.GET,
            self._url(),
            json={"transactions": [{"type": "WAIVER"}]},
        )
        data = self._league().transactions()
        assert data["transactions"][0]["type"] == "WAIVER"
        assert "view=mTransactions2" in responses.calls[0].request.url
