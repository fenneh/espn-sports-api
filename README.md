# espn-sports-api

Python client for ESPN's public API. No authentication required for most endpoints.

## Installation

```bash
pip install espn-sports-api
```

## Quick Start

```python
from espn_sports_api import NFL, NBA, Soccer

# Get today's NFL scores
nfl = NFL()
scores = nfl.scoreboard()

# Get NBA team roster
nba = NBA()
roster = nba.team_roster("lal")  # Lakers

# Get Premier League table
epl = Soccer(league="epl")
table = epl.standings()
```

## Supported Sports

| Sport | Class | Leagues/Tours |
|-------|-------|---------------|
| Football | `NFL`, `NCAAF` | NFL, College Football |
| Basketball | `NBA`, `NCAAB`, `WNBA` | NBA, College Basketball, WNBA |
| Baseball | `MLB` | MLB |
| Hockey | `NHL` | NHL |
| Soccer | `Soccer` | EPL, La Liga, Bundesliga, Serie A, MLS, Champions League, etc. |
| MMA | `UFC` | UFC |
| Golf | `Golf` | PGA, LPGA, European Tour |
| Racing | `Racing` | F1, NASCAR, IndyCar |
| Tennis | `Tennis` | ATP, WTA |

## Common Methods

All sport classes share these methods:

```python
sport.scoreboard(dates="20240115")  # Get scores for specific date
sport.teams()                        # Get all teams
sport.team("NYY")                    # Get team by ID/abbreviation
sport.team_roster("NYY")             # Get team roster
sport.team_schedule("NYY")           # Get team schedule
sport.standings()                    # Get standings
sport.news()                         # Get news articles
sport.event("401547417")             # Get game/event details
```

## Soccer Leagues

```python
from espn_sports_api import Soccer

# Use league name
epl = Soccer(league="epl")
la_liga = Soccer(league="la_liga")
mls = Soccer(league="mls")

# Or ESPN code directly
bundesliga = Soccer(league="ger.1")

# Available leagues
print(Soccer.available_leagues())
```

## Racing

```python
from espn_sports_api import Racing

f1 = Racing(series="f1")
nascar = Racing(series="nascar")
indycar = Racing(series="indycar")

# Get standings
standings = f1.standings()

# Get schedule
schedule = f1.schedule(season=2024)
```

## Fantasy Leagues

For private leagues, you'll need your ESPN cookies (`SWID` and `espn_s2`).

```python
from espn_sports_api import FantasyFootball

# Public league
league = FantasyFootball(league_id=123456, season=2024)

# Private league
league = FantasyFootball(
    league_id=123456,
    season=2024,
    swid="{YOUR-SWID}",
    espn_s2="YOUR_ESPN_S2_COOKIE"
)

teams = league.teams()
matchups = league.matchups(week=1)
standings = league.standings()
```

## Context Manager

All classes support context managers for automatic cleanup:

```python
with NFL() as nfl:
    scores = nfl.scoreboard()
```

## API Reference

ESPN's public API doesn't require authentication. The base URLs used:

- `site.api.espn.com` - Scoreboards, teams, standings
- `sports.core.api.espn.com` - Athletes, detailed stats
- `lm-api-reads.fantasy.espn.com` - Fantasy leagues

## License

MIT
