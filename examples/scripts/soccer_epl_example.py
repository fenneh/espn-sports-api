#!/usr/bin/env python3
"""
Premier League Example Script
=============================

This script demonstrates how to use espn-sports-api to fetch
English Premier League (EPL) data.

Run this script:
    python examples/soccer_epl_example.py

Requirements:
    pip install espn-sports-api
"""

from datetime import date, timedelta

from espn_sports_api import Soccer, quick_scores


def basic_usage():
    """
    BASIC USAGE
    -----------
    The simplest way to get Premier League scores.
    """
    print("=" * 60)
    print("BASIC USAGE")
    print("=" * 60)

    # One-liner for today's EPL scores
    scores = quick_scores("epl")
    print(f"\nFound {len(scores.get('events', []))} EPL matches today")

    # Or create a Soccer instance for EPL
    epl = Soccer(league="epl")
    today_matches = epl.today()

    for event in today_matches.get("events", []):
        print(f"  - {event['name']}")


def get_live_matches():
    """
    LIVE MATCHES
    ------------
    Get matches currently in progress.
    """
    print("\n" + "=" * 60)
    print("LIVE MATCHES")
    print("=" * 60)

    epl = Soccer(league="epl")
    live = epl.live()

    matches = live.get("events", [])
    if not matches:
        print("\nNo matches in progress right now.")
    else:
        print(f"\n{len(matches)} match(es) in progress:")
        for event in matches:
            comp = event.get("competitions", [{}])[0]
            competitors = comp.get("competitors", [])

            if len(competitors) == 2:
                away = next((c for c in competitors if c["homeAway"] == "away"), {})
                home = next((c for c in competitors if c["homeAway"] == "home"), {})

                away_team = away.get("team", {}).get("shortDisplayName", "???")
                home_team = home.get("team", {}).get("shortDisplayName", "???")
                away_score = away.get("score", "0")
                home_score = home.get("score", "0")

                # Get match clock if available
                status = comp.get("status", {})
                clock = status.get("displayClock", "")
                period = status.get("period", 0)
                time_display = f"{clock} ({period}H)" if clock else ""

                print(f"  {home_team} {home_score} - {away_score} {away_team} {time_display}")


def get_league_table():
    """
    LEAGUE TABLE
    ------------
    Get the current Premier League standings.
    """
    print("\n" + "=" * 60)
    print("PREMIER LEAGUE TABLE")
    print("=" * 60)

    epl = Soccer(league="epl")

    # Use the table() method for soccer standings
    table_data = epl.table()

    standings = table_data.get("children", [{}])[0].get("standings", {})
    entries = standings.get("entries", [])

    print(f"\n{'Pos':<4} {'Team':<25} {'P':>3} {'W':>3} {'D':>3} {'L':>3} {'GD':>4} {'Pts':>4}")
    print("-" * 55)

    for entry in entries[:10]:  # Top 10
        team = entry.get("team", {}).get("displayName", "Unknown")
        stats = {s["name"]: s["value"] for s in entry.get("stats", [])}

        pos = int(stats.get("rank", 0))
        played = int(stats.get("gamesPlayed", 0))
        wins = int(stats.get("wins", 0))
        draws = int(stats.get("ties", 0))
        losses = int(stats.get("losses", 0))
        gd = int(stats.get("pointDifferential", 0))
        points = int(stats.get("points", 0))

        row = f"{pos:<4} {team:<25} {played:>3} {wins:>3} {draws:>3} {losses:>3}"
        print(f"{row} {gd:>+4} {points:>4}")


def get_team_info():
    """
    TEAM INFORMATION
    ----------------
    Get details about a specific team.
    """
    print("\n" + "=" * 60)
    print("TEAM INFORMATION")
    print("=" * 60)

    epl = Soccer(league="epl")

    # Get team details - use team ID or slug
    team_data = epl.team("364")  # Arsenal's team ID
    team = team_data.get("team", {})

    print(f"\nTeam: {team.get('displayName')}")
    print(f"Nickname: {team.get('nickname', 'N/A')}")
    print(f"Location: {team.get('location')}")
    print(f"Abbreviation: {team.get('abbreviation')}")

    # Venue info
    venue = team.get("franchise", {}).get("venue", {})
    if venue:
        print(f"Stadium: {venue.get('fullName')}")
        capacity = venue.get("capacity")
        if capacity:
            print(f"Capacity: {capacity:,}")


def get_team_roster():
    """
    TEAM ROSTER / SQUAD
    -------------------
    List players in a team's squad.
    """
    print("\n" + "=" * 60)
    print("TEAM SQUAD")
    print("=" * 60)

    epl = Soccer(league="epl")
    roster_data = epl.team_roster("360")  # Manchester City

    athletes = roster_data.get("athletes", [])
    all_players = []

    for group in athletes:
        position = group.get("position", "Unknown")
        for player in group.get("items", []):
            all_players.append(
                {
                    "name": player.get("displayName"),
                    "number": player.get("jersey", "-"),
                    "position": position,
                    "nationality": player.get("citizenship", ""),
                }
            )

    print(f"\nManchester City squad ({len(all_players)} players):")
    for player in all_players[:15]:
        nat = f" ({player['nationality']})" if player["nationality"] else ""
        print(f"  #{player['number']:>2} {player['name']} - {player['position']}{nat}")


def get_fixtures():
    """
    FIXTURES
    --------
    Get upcoming matches for the league or a team.
    """
    print("\n" + "=" * 60)
    print("UPCOMING FIXTURES")
    print("=" * 60)

    epl = Soccer(league="epl")

    # Get this weekend's matches
    today = date.today()
    weekend_end = today + timedelta(days=7)
    fixtures = epl.date_range(today, weekend_end)

    events = fixtures.get("events", [])
    print(f"\nNext 7 days ({len(events)} matches):")

    for event in events[:10]:
        name = event.get("name", "Unknown")
        event_date = event.get("date", "")[:10]
        venue = event.get("competitions", [{}])[0].get("venue", {}).get("fullName", "")

        print(f"  {event_date}: {name}")
        if venue:
            print(f"              @ {venue}")


def get_team_schedule():
    """
    TEAM SCHEDULE
    -------------
    Get a specific team's fixtures.
    """
    print("\n" + "=" * 60)
    print("TEAM SCHEDULE")
    print("=" * 60)

    epl = Soccer(league="epl")
    schedule = epl.team_schedule("359")  # Liverpool

    events = schedule.get("events", [])
    print(f"\nLiverpool fixtures ({len(events)} matches):")

    for event in events[:8]:
        name = event.get("name", "Unknown")
        event_date = event.get("date", "")[:10]
        status = event.get("status", {}).get("type", {}).get("description", "")

        # Check if it's a completed game
        comp = event.get("competitions", [{}])[0]
        competitors = comp.get("competitors", [])
        score = ""

        if status == "Final" and len(competitors) == 2:
            home = next((c for c in competitors if c["homeAway"] == "home"), {})
            away = next((c for c in competitors if c["homeAway"] == "away"), {})
            score = f" ({home.get('score', '?')}-{away.get('score', '?')})"

        print(f"  {event_date}: {name}{score} - {status}")


def explore_other_leagues():
    """
    OTHER LEAGUES
    -------------
    The Soccer class supports 90+ leagues worldwide.
    """
    print("\n" + "=" * 60)
    print("OTHER LEAGUES")
    print("=" * 60)

    # Show available leagues
    all_leagues = Soccer.available_leagues()
    print(f"\n{len(all_leagues)} leagues available. Examples:")

    sample_leagues = ["la_liga", "bundesliga", "serie_a", "ligue_1", "mls", "champions_league"]

    for league_key in sample_leagues:
        if league_key in all_leagues:
            print(f"  - {league_key}: {all_leagues[league_key]}")

    # Quick example with another league
    print("\nLa Liga today:")
    la_liga = Soccer(league="la_liga")
    today = la_liga.today()

    for event in today.get("events", [])[:3]:
        print(f"  - {event['name']}")


def get_match_details():
    """
    MATCH DETAILS
    -------------
    Get detailed information about a specific match.
    """
    print("\n" + "=" * 60)
    print("MATCH DETAILS")
    print("=" * 60)

    epl = Soccer(league="epl")

    # First, find a recent match from the scoreboard
    recent = epl.yesterday()
    events = recent.get("events", [])

    if not events:
        # Try today if no matches yesterday
        recent = epl.today()
        events = recent.get("events", [])

    if not events:
        print("\nNo recent matches to show details for.")
        return

    # Get details for the first match
    event_id = events[0]["id"]
    details = epl.event(event_id)

    # Extract key information
    boxscore = details.get("boxscore", {})
    teams = boxscore.get("teams", [])

    print(f"\nMatch: {events[0]['name']}")

    for team_data in teams:
        team = team_data.get("team", {})
        stats = team_data.get("statistics", [])

        print(f"\n  {team.get('displayName')}:")
        for stat in stats[:5]:  # Show first 5 stats
            print(f"    {stat.get('label', 'N/A')}: {stat.get('displayValue', 'N/A')}")


def list_all_teams():
    """
    ALL TEAMS
    ---------
    List all teams in the Premier League.
    """
    print("\n" + "=" * 60)
    print("ALL PREMIER LEAGUE TEAMS")
    print("=" * 60)

    epl = Soccer(league="epl")
    teams_data = epl.teams()

    # Navigate the response structure
    sports = teams_data.get("sports", [])
    all_teams = []

    for sport in sports:
        for league in sport.get("leagues", []):
            for team_entry in league.get("teams", []):
                team = team_entry.get("team", team_entry)
                all_teams.append(
                    {
                        "id": team.get("id"),
                        "name": team.get("displayName"),
                        "abbr": team.get("abbreviation"),
                    }
                )

    print(f"\nPremier League teams ({len(all_teams)}):")
    for team in sorted(all_teams, key=lambda t: t["name"]):
        print(f"  {team['abbr']:<5} {team['name']} (ID: {team['id']})")


if __name__ == "__main__":
    print("\nESPN Sports API - Premier League Examples")
    print("=" * 60)

    # Run all examples
    basic_usage()
    get_live_matches()
    get_league_table()
    get_team_info()
    get_team_roster()
    get_fixtures()
    get_team_schedule()
    explore_other_leagues()
    get_match_details()
    list_all_teams()

    print("\n" + "=" * 60)
    print("Examples complete!")
    print("=" * 60)
