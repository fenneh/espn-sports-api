"""Data models for ESPN API responses."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Venue:
    """Stadium/venue information."""

    id: str
    name: str
    city: str
    state: str
    country: str
    capacity: Optional[int] = None
    indoor: bool = False
    grass: bool = True

    def __str__(self) -> str:
        location = f"{self.city}, {self.state}" if self.state else self.city
        cap = f" ({self.capacity:,} capacity)" if self.capacity else ""
        return f"{self.name} - {location}{cap}"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Venue":
        """Create Venue from API response dict."""
        address = data.get("address", {})
        return cls(
            id=str(data.get("id", "")),
            name=data.get("fullName", data.get("name", "")),
            city=address.get("city", ""),
            state=address.get("state", ""),
            country=address.get("country", ""),
            capacity=data.get("capacity"),
            indoor=data.get("indoor", False),
            grass=data.get("grass", True),
        )


@dataclass
class Broadcast:
    """TV broadcast information."""

    network: str
    market: str
    language: str
    region: str

    def __str__(self) -> str:
        return self.network

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Broadcast":
        """Create Broadcast from API response dict."""
        return cls(
            network=data.get("names", [""])[0] if data.get("names") else "",
            market=data.get("market", ""),
            language=data.get("lang", "en"),
            region=data.get("region", ""),
        )


@dataclass
class Weather:
    """Game weather conditions."""

    temperature: int
    conditions: str
    high_temp: Optional[int] = None
    low_temp: Optional[int] = None

    def __str__(self) -> str:
        return f"{self.temperature}°F, {self.conditions}"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Weather":
        """Create Weather from API response dict."""
        return cls(
            temperature=data.get("temperature", 0),
            conditions=data.get("displayValue", data.get("conditionId", "")),
            high_temp=data.get("highTemperature"),
            low_temp=data.get("lowTemperature"),
        )


@dataclass
class Injury:
    """Player injury information."""

    athlete_id: str
    athlete_name: str
    team: str
    position: str
    status: str
    injury_type: str
    body_part: str
    description: str
    return_date: Optional[str] = None

    def __str__(self) -> str:
        injury = self.injury_type or self.body_part
        return f"{self.athlete_name} ({self.position}, {self.team}): {self.status} - {injury}"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Injury":
        """Create Injury from API response dict."""
        athlete = data.get("athlete", {})
        details = data.get("details", {})
        return cls(
            athlete_id=str(athlete.get("id", "")),
            athlete_name=athlete.get("displayName", ""),
            team=athlete.get("team", {}).get("displayName", ""),
            position=athlete.get("position", {}).get("abbreviation", ""),
            status=data.get("status", ""),
            injury_type=details.get("type", ""),
            body_part=details.get("location", ""),
            description=data.get("longComment", data.get("shortComment", "")),
            return_date=details.get("returnDate"),
        )


@dataclass
class Transaction:
    """Player transaction (trade, signing, etc.)."""

    id: str
    date: str
    transaction_type: str
    description: str
    team: str
    athlete_name: Optional[str] = None

    def __str__(self) -> str:
        player = f"{self.athlete_name} - " if self.athlete_name else ""
        return f"{self.date}: {player}{self.team} - {self.transaction_type}"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Transaction":
        """Create Transaction from API response dict."""
        return cls(
            id=str(data.get("id", "")),
            date=data.get("date", ""),
            transaction_type=data.get("type", {}).get("text", ""),
            description=data.get("description", ""),
            team=data.get("team", {}).get("displayName", ""),
            athlete_name=data.get("athlete", {}).get("displayName"),
        )


@dataclass
class Athlete:
    """Athlete/player information."""

    id: str
    name: str
    first_name: str
    last_name: str
    jersey: Optional[str] = None
    position: str = ""
    team: str = ""
    height: str = ""
    weight: int = 0
    age: Optional[int] = None
    college: str = ""
    birthplace: str = ""
    experience: int = 0
    headshot_url: Optional[str] = None

    def __str__(self) -> str:
        jersey = f"#{self.jersey} " if self.jersey else ""
        pos_team = f"({self.position}, {self.team})" if self.position and self.team else ""
        return f"{jersey}{self.name} {pos_team}".strip()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Athlete":
        """Create Athlete from API response dict."""
        birthplace = data.get("birthPlace", {})
        bp_str = ""
        if birthplace:
            state_or_country = birthplace.get("state", birthplace.get("country", ""))
            bp_str = f"{birthplace.get('city', '')}, {state_or_country}"

        return cls(
            id=str(data.get("id", "")),
            name=data.get("displayName", data.get("fullName", "")),
            first_name=data.get("firstName", ""),
            last_name=data.get("lastName", ""),
            jersey=data.get("jersey"),
            position=data.get("position", {}).get("abbreviation", ""),
            team=data.get("team", {}).get("displayName", ""),
            height=data.get("displayHeight", ""),
            weight=data.get("weight", 0),
            age=data.get("age"),
            college=data.get("college", {}).get("name", ""),
            birthplace=bp_str,
            experience=data.get("experience", {}).get("years", 0),
            headshot_url=data.get("headshot", {}).get("href"),
        )


@dataclass
class Team:
    """Team information."""

    id: str
    name: str
    abbreviation: str
    location: str
    nickname: str
    color: str
    alternate_color: str
    logo_url: Optional[str] = None
    record: str = ""
    standing: str = ""

    def __str__(self) -> str:
        record = f" ({self.record})" if self.record else ""
        return f"{self.name} ({self.abbreviation}){record}"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Team":
        """Create Team from API response dict."""
        logos = data.get("logos", [])
        logo_url = logos[0].get("href") if logos else None

        record = ""
        record_items = data.get("record", {}).get("items", [])
        if record_items:
            record = record_items[0].get("summary", "")

        return cls(
            id=str(data.get("id", "")),
            name=data.get("displayName", ""),
            abbreviation=data.get("abbreviation", ""),
            location=data.get("location", ""),
            nickname=data.get("nickname", data.get("name", "")),
            color=data.get("color", ""),
            alternate_color=data.get("alternateColor", ""),
            logo_url=logo_url,
            record=record,
            standing=data.get("standingSummary", ""),
        )


def parse_injuries(response: dict[str, Any]) -> list[Injury]:
    """Parse injuries from API response.

    Args:
        response: Injuries API response.

    Returns:
        List of Injury objects.
    """
    items = response.get("items", response.get("injuries", []))
    return [Injury.from_dict(item) for item in items]


def parse_transactions(response: dict[str, Any]) -> list[Transaction]:
    """Parse transactions from API response.

    Args:
        response: Transactions API response.

    Returns:
        List of Transaction objects.
    """
    items = response.get("items", response.get("transactions", []))
    return [Transaction.from_dict(item) for item in items]


def parse_venues(response: dict[str, Any]) -> list[Venue]:
    """Parse venues from API response.

    Args:
        response: Venues API response.

    Returns:
        List of Venue objects.
    """
    items = response.get("items", response.get("venues", []))
    return [Venue.from_dict(item) for item in items]


def parse_athletes(response: dict[str, Any]) -> list[Athlete]:
    """Parse athletes from API response.

    Args:
        response: Athletes API response.

    Returns:
        List of Athlete objects.
    """
    items = response.get("items", response.get("athletes", []))
    return [Athlete.from_dict(item) for item in items]


def parse_teams(response: dict[str, Any]) -> list[Team]:
    """Parse teams from API response.

    Args:
        response: Teams API response.

    Returns:
        List of Team objects.
    """
    sports = response.get("sports", [])
    teams = []
    for sport in sports:
        for league in sport.get("leagues", []):
            for team in league.get("teams", []):
                team_data = team.get("team", team)
                teams.append(Team.from_dict(team_data))
    return teams
