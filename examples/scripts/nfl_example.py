#!/usr/bin/env python3
"""
NFL Example Script
==================

This script demonstrates how to use espn-sports-api to fetch NFL data.
Each section builds on the previous one, starting with the basics.

Run this script:
    python examples/nfl_example.py

Requirements:
    pip install espn-sports-api
"""

from datetime import date

from espn_sports_api import NFL, Odds, parse_injuries, parse_teams, quick_scores


def basic_usage():
    """
    BASIC USAGE
    -----------
    The simplest way to get NFL scores.
    """
    print("=" * 60)
    print("BASIC USAGE")
    print("=" * 60)

    # One-liner to get today's scores (works for any sport)
    scores = quick_scores("nfl")
    print(f"\nFound {len(scores.get('events', []))} games today")

    # Or create an NFL instance for more control
    nfl = NFL()
    today_games = nfl.today()

    for event in today_games.get("events", []):
        print(f"  - {event['name']}")


def get_live_games():
    """
    LIVE GAMES
    ----------
    Filter to only show games currently in progress.
    """
    print("\n" + "=" * 60)
    print("LIVE GAMES")
    print("=" * 60)

    nfl = NFL()
    live = nfl.live()

    games = live.get("events", [])
    if not games:
        print("\nNo games in progress right now.")
    else:
        print(f"\n{len(games)} game(s) in progress:")
        for event in games:
            # Get the score from competitions
            comp = event.get("competitions", [{}])[0]
            competitors = comp.get("competitors", [])

            if len(competitors) == 2:
                away = next((c for c in competitors if c["homeAway"] == "away"), {})
                home = next((c for c in competitors if c["homeAway"] == "home"), {})

                away_team = away.get("team", {}).get("abbreviation", "???")
                home_team = home.get("team", {}).get("abbreviation", "???")
                away_score = away.get("score", "0")
                home_score = home.get("score", "0")

                print(f"  {away_team} {away_score} @ {home_team} {home_score}")


def get_team_info():
    """
    TEAM INFORMATION
    ----------------
    Get details about a specific team.
    """
    print("\n" + "=" * 60)
    print("TEAM INFORMATION")
    print("=" * 60)

    nfl = NFL()

    # Get team details using abbreviation
    team_data = nfl.team("kc")  # Kansas City Chiefs
    team = team_data.get("team", {})

    print(f"\nTeam: {team.get('displayName')}")
    print(f"Location: {team.get('location')}")
    print(f"Abbreviation: {team.get('abbreviation')}")
    print(f"Conference: {team.get('standingSummary', 'N/A')}")

    # Get venue info if available
    venue = team.get("franchise", {}).get("venue", {})
    if venue:
        print(f"Stadium: {venue.get('fullName')}")


def get_team_roster():
    """
    TEAM ROSTER
    -----------
    List all players on a team.
    """
    print("\n" + "=" * 60)
    print("TEAM ROSTER (First 10 players)")
    print("=" * 60)

    nfl = NFL()
    roster_data = nfl.team_roster("buf")  # Buffalo Bills

    # Roster is grouped by position
    athletes = roster_data.get("athletes", [])
    all_players = []

    for group in athletes:
        position = group.get("position", "Unknown")
        for player in group.get("items", []):
            all_players.append(
                {
                    "name": player.get("displayName"),
                    "number": player.get("jersey", "N/A"),
                    "position": position,
                }
            )

    print(f"\nBuffalo Bills roster ({len(all_players)} players):")
    for player in all_players[:10]:
        print(f"  #{player['number']:>2} {player['name']} ({player['position']})")


def get_schedule():
    """
    TEAM SCHEDULE
    -------------
    Get a team's upcoming and past games.
    """
    print("\n" + "=" * 60)
    print("TEAM SCHEDULE")
    print("=" * 60)

    nfl = NFL()
    schedule_data = nfl.team_schedule("phi")  # Philadelphia Eagles

    events = schedule_data.get("events", [])
    print(f"\nPhiladelphia Eagles schedule ({len(events)} games):")

    for event in events[:5]:  # Show first 5 games
        name = event.get("name", "Unknown")
        event_date = event.get("date", "")[:10]  # Just the date part
        status = event.get("status", {}).get("type", {}).get("description", "")
        print(f"  {event_date}: {name} - {status}")


def get_standings():
    """
    STANDINGS
    ---------
    Get current NFL standings by division.
    """
    print("\n" + "=" * 60)
    print("STANDINGS")
    print("=" * 60)

    nfl = NFL()
    standings_data = nfl.standings()

    children = standings_data.get("children", [])
    if children:
        # Show first conference/division
        conf = children[0]
        print(f"\n{conf.get('name', 'Conference')}:")

        for division in conf.get("children", [])[:2]:  # First 2 divisions
            print(f"\n  {division.get('name', 'Division')}:")

            for entry in division.get("standings", {}).get("entries", []):
                team_name = entry.get("team", {}).get("displayName", "Unknown")
                stats = entry.get("stats", [])

                # Find wins and losses
                wins = next((s["value"] for s in stats if s["name"] == "wins"), 0)
                losses = next((s["value"] for s in stats if s["name"] == "losses"), 0)

                print(f"    {team_name}: {int(wins)}-{int(losses)}")


def get_injuries():
    """
    INJURIES
    --------
    Get injury reports using the data models.
    """
    print("\n" + "=" * 60)
    print("INJURIES")
    print("=" * 60)

    nfl = NFL()
    injury_data = nfl.injuries()

    # Use the parse_injuries helper to get Injury objects
    injuries = parse_injuries(injury_data)

    print(f"\nLeague-wide injuries ({len(injuries)} total):")
    for injury in injuries[:10]:  # Show first 10
        # The Injury model has a nice __str__ method
        print(f"  {injury}")


def get_betting_odds():
    """
    BETTING ODDS
    ------------
    Extract betting lines from scoreboard data.
    """
    print("\n" + "=" * 60)
    print("BETTING ODDS")
    print("=" * 60)

    nfl = NFL()
    scoreboard = nfl.scoreboard()

    # Use the Odds helper class
    all_odds = Odds.from_scoreboard(scoreboard)

    if not all_odds:
        print("\nNo odds available (games may have started or finished).")
        return

    print(f"\nOdds for {len(all_odds)} games:")
    for game in all_odds[:5]:  # Show first 5
        print(f"\n  {game.away_team} @ {game.home_team}")

        if game.spread:
            print(f"    Spread: {game.spread.favorite} {game.spread.spread}")

        if game.moneyline:
            print(f"    Moneyline: {game.moneyline.home_odds}/{game.moneyline.away_odds}")

        if game.total:
            print(f"    Over/Under: {game.total.over_under}")


def get_historical_games():
    """
    HISTORICAL DATA
    ---------------
    Look up games from specific dates or weeks.
    """
    print("\n" + "=" * 60)
    print("HISTORICAL DATA")
    print("=" * 60)

    nfl = NFL()

    # Get games from a specific date
    christmas = nfl.on_date(date(2024, 12, 25))
    print(f"\nChristmas 2024 games: {len(christmas.get('events', []))} games")

    # Get games from Week 1
    week1 = nfl.for_week(1)
    print(f"Week 1 games: {len(week1.get('events', []))} games")


def list_all_teams():
    """
    ALL TEAMS
    ---------
    Get a list of all NFL teams using data models.
    """
    print("\n" + "=" * 60)
    print("ALL NFL TEAMS")
    print("=" * 60)

    nfl = NFL()
    teams_data = nfl.teams()

    # Use parse_teams helper for Team objects
    teams = parse_teams(teams_data)

    print(f"\nAll NFL teams ({len(teams)}):")
    for team in sorted(teams, key=lambda t: t.name):
        # Team model has a nice __str__ method
        print(f"  {team}")


if __name__ == "__main__":
    print("\nESPN Sports API - NFL Examples")
    print("=" * 60)

    # Run all examples
    basic_usage()
    get_live_games()
    get_team_info()
    get_team_roster()
    get_schedule()
    get_standings()
    get_injuries()
    get_betting_odds()
    get_historical_games()
    list_all_teams()

    print("\n" + "=" * 60)
    print("Examples complete!")
    print("=" * 60)
