"""
Data model definitions for the pilgrimage route planner, including travel modes and spot representation.
"""

from dataclasses import dataclass
from enum import Enum


class TravelMode(str, Enum):
    """Google Maps travel modes, values match the `travel mode` query parameter."""

    DRIVING = "driving"
    WALKING = "walking"
    BICYCLING = "bicycling"
    TRANSIT = "transit"


@dataclass
class Spot:
    """Represents a spot with an optional Google Maps short URL and coordinates."""

    name: str
    maps_url: str
    label: str | None = None
    coordinates: tuple[float, float] | None = None
