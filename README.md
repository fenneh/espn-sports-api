# espn-sports-api

[![PyPI](https://img.shields.io/pypi/v/espn-sports-api)](https://pypi.org/project/espn-sports-api/)
[![CI](https://github.com/fenneh/espn-sports-api/actions/workflows/ci.yml/badge.svg)](https://github.com/fenneh/espn-sports-api/actions/workflows/ci.yml)
[![Python](https://img.shields.io/pypi/pyversions/espn-sports-api)](https://pypi.org/project/espn-sports-api/)
[![License](https://img.shields.io/pypi/l/espn-sports-api)](https://github.com/fenneh/espn-sports-api/blob/main/LICENSE)

Python client for ESPN's public API. No authentication required for most endpoints.

## Installation

```bash
uv add espn-sports-api
```

or with pip:

```bash
pip install espn-sports-api
```

## Quick Start

```python
from espn_sports_api import NFL, NBA, Soccer, quick_scores

# One-liner for today's scores
scores = quick_scores("nba")

# Get today's NFL scores
nfl = NFL()
scores = nfl.today()

# Get NBA team roster
nba = NBA()
roster = nba.team_roster("lal")

# Get Premier League table
epl = Soccer(league="epl")
table = epl.standings()
```

## Supported Sports

| Sport | Class | Leagues |
|-------|-------|---------|
| Football | `NFL`, `NCAAF`, `CFL`, `XFL` | NFL, College Football, CFL, XFL |
| Basketball | `NBA`, `NCAAB`, `WomensNCAAB`, `WNBA` | NBA, College Basketball, WNBA |
| Baseball | `MLB`, `CollegeBaseball` | MLB, College Baseball |
| Hockey | `NHL` | NHL |
| Soccer | `Soccer` | 90+ leagues worldwide |
| MMA | `UFC` | UFC |
| Golf | `Golf` | PGA, LPGA, European Tour |
| Racing | `Racing` | F1, NASCAR, IndyCar |
| Tennis | `Tennis` | ATP, WTA |

## Common Methods

All sport classes share these methods:

```python
# Scoreboard with filtering
sport.scoreboard(dates="20240115")       # By date
sport.scoreboard(season=2024, week=10)   # By season/week
sport.scoreboard(seasontype=2)           # 1=pre, 2=regular, 3=post

# Teams
sport.teams()                  # All teams
sport.team("NYY")              # Team details
sport.team_roster("NYY")       # Team roster
sport.team_schedule("NYY")     # Team schedule
sport.team_injuries("NYY")     # Team injuries

# League-wide data
sport.injuries()               # All injuries
sport.transactions()           # Trades, signings, IR moves
sport.statistics()             # League statistics
sport.leaders()                # Statistical leaders
sport.venues()                 # Stadium information
sport.franchises()             # Franchise data
sport.events()                 # All games
sport.positions()              # All positions

# Other
sport.standings()              # Standings
sport.news()                   # News articles
sport.event("401547417")       # Game details
sport.playbyplay("401547417")  # Play-by-play data
sport.athlete("12345")         # Athlete profile
sport.athlete_stats("12345")   # Athlete statistics
sport.seasons(2024)            # Season information

# Date convenience methods
sport.today()                  # Today's games
sport.yesterday()              # Yesterday's games
sport.tomorrow()               # Tomorrow's games
sport.live()                   # In-progress games only
sport.on_date(date(2024,12,25)) # Games on specific date
sport.date_range(start, end)   # Games in date range
sport.for_week(10, season=2024) # Games for specific week
```

## College Conference Filtering

Filter college sports by conference:

```python
from espn_sports_api import NCAAF, NCAAB, NCAAFConference, Conferences

# By string name
ncaaf = NCAAF()
sec_games = ncaaf.scoreboard(conference="SEC")
big_ten = ncaaf.scoreboard(conference="Big Ten")

# By enum (type-safe)
ncaab = NCAAB()
games = ncaab.scoreboard(conference=NCAABConference.BIG_EAST)

# Lookup conference IDs
Conferences.get("ncaaf", "SEC")          # Returns 8
Conferences.get("ncaab", "Big Ten")      # Returns 7
Conferences.list_all("ncaaf")            # All NCAAF conferences
```

## Betting Odds

Extract odds from scoreboard responses:

```python
from espn_sports_api import NFL, Odds

nfl = NFL()
scoreboard = nfl.scoreboard()

# Get all odds
all_odds = Odds.from_scoreboard(scoreboard)
for game in all_odds:
    print(f"{game.away_team} @ {game.home_team}")
    if game.spread:
        print(f"  Spread: {game.spread.favorite} {game.spread.spread}")
    if game.moneyline:
        print(f"  ML: {game.moneyline.home_odds}/{game.moneyline.away_odds}")
    if game.total:
        print(f"  O/U: {game.total.over_under}")

# Or get specific data
spreads = Odds.spreads(scoreboard)
moneylines = Odds.moneylines(scoreboard)
totals = Odds.totals(scoreboard)
```

## Data Models

Parse API responses into dataclasses:

```python
from espn_sports_api import NFL, parse_injuries, parse_teams

nfl = NFL()

# Parse injuries - models have readable __str__ methods
injury_response = nfl.injuries()
injuries = parse_injuries(injury_response)
for injury in injuries:
    print(injury)  # "John Doe (QB, Patriots): Questionable - Ankle"

# Parse teams
teams_response = nfl.teams()
teams = parse_teams(teams_response)
for team in teams:
    print(f"{team.name} ({team.abbreviation})")
```

Available models: `Venue`, `Broadcast`, `Weather`, `Injury`, `Transaction`, `Athlete`, `Team`

## Soccer Leagues

90+ leagues supported:

```python
from espn_sports_api import Soccer

# Major leagues
epl = Soccer(league="epl")
la_liga = Soccer(league="la_liga")
bundesliga = Soccer(league="bundesliga")
serie_a = Soccer(league="serie_a")
ligue_1 = Soccer(league="ligue_1")
mls = Soccer(league="mls")

# Cups and competitions
champions_league = Soccer(league="champions_league")
europa_league = Soccer(league="europa_league")
fa_cup = Soccer(league="fa_cup")
copa_libertadores = Soccer(league="copa_libertadores")
world_cup = Soccer(league="world_cup")

# International
liga_mx = Soccer(league="liga_mx")
eredivisie = Soccer(league="eredivisie")
scottish_premiership = Soccer(league="scottish_premiership")
j_league = Soccer(league="j_league")

# All available leagues
print(Soccer.available_leagues())

# Cross-league scoreboard
all_scores = Soccer.all_leagues_scoreboard(dates="20240115")
```

## Racing

```python
from espn_sports_api import Racing

f1 = Racing(series="f1")
nascar = Racing(series="nascar")
indycar = Racing(series="indycar")

standings = f1.standings()
schedule = f1.schedule(season=2024)
```

## Fantasy Leagues

```python
from espn_sports_api import FantasyFootball

# Public league
league = FantasyFootball(league_id=123456, season=2024)

# Private league (requires cookies)
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

## Caching

Enable response caching for faster repeated requests:

```python
from espn_sports_api import ESPNClient, NFL
from pathlib import Path

# Memory cache with 5-minute TTL
client = ESPNClient(cache_ttl=300)
nfl = NFL(client=client)

# First request hits the API
scores = nfl.scoreboard()  # ~300ms

# Second request uses cache
scores = nfl.scoreboard()  # ~0ms

# Clear cache when needed
client.clear_cache()

# Disk cache for persistence across sessions
client = ESPNClient(cache_ttl=3600, cache_dir=Path("./cache"))
```

## Context Manager

```python
with NFL() as nfl:
    scores = nfl.scoreboard()
```

## Examples

**Interactive Notebook** - explore the API without installing anything:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/fenneh/espn-sports-api/blob/main/examples/notebooks/explore_sports_data.ipynb)
[![Deepnote](https://deepnote.com/buttons/launch-in-deepnote-small.svg)](https://deepnote.com/launch?url=https://github.com/fenneh/espn-sports-api/blob/main/examples/notebooks/explore_sports_data.ipynb)

Or run the Python scripts locally:

```bash
python examples/scripts/nfl_example.py
python examples/scripts/soccer_epl_example.py
```

## API Reference

ESPN's public API doesn't require authentication. Base URLs:

- `site.api.espn.com` - Scoreboards, teams, standings, news, injuries, transactions
- `sports.core.api.espn.com` - Athletes, venues, franchises, events, leaders
- `site.web.api.espn.com` - Athlete statistics
- `lm-api-reads.fantasy.espn.com` - Fantasy leagues

## License

MIT
