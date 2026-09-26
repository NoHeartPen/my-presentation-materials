"""
Main module for pilgrimage route planning,
including functions for parsing coordinates,
calculating distances, generating Google Maps URLs, and planning routes.
"""

from __future__ import annotations

import math
import re
import urllib.parse

import requests

from data_model import Spot, TravelMode


def coordinates_from_google_maps(short_url: str) -> tuple[float, float]:
    """Parse latitude and longitude coordinates from a Google Maps short URL."""
    response = requests.get(
        short_url,
        allow_redirects=True,
        timeout=15,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    response.raise_for_status()

    # use the !3d<latitude>!4d<longitude> pattern first
    match = re.search(
        r"!3d(-?\d+(?:\.\d+)?)!4d(-?\d+(?:\.\d+)?)",
        response.url,
    )

    # fallback to the map view format: @<latitude>,<longitude>
    if not match:
        match = re.search(
            r"@(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)",
            response.url,
        )

    if not match:
        raise ValueError(f"Failed to parse coordinates from URL: {response.url}")

    lat_str, lon_str = match.groups()
    return (float(lat_str), float(lon_str))


def gps_distance_m(point_a: tuple[float, float], point_b: tuple[float, float]) -> float:
    """Calculate the distance between two latitude/longitude coordinates using the Haversine formula (in meters)."""
    earth_radius_m = 6371000.0
    lat1, lon1 = point_a
    lat2, lon2 = point_b

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return earth_radius_m * c


def generate_google_maps_url(
    origin: Spot,
    destination: Spot,
    waypoints: list[Spot] | None = None,
    travel_mode: TravelMode = TravelMode.WALKING,
) -> str:
    """Generate a Google Maps URL for the given route."""
    base_url = "https://www.google.com/maps/dir/?api=1"
    params = {
        "origin": origin.name,
        "destination": destination.name,
        "travelmode": travel_mode.value,
    }
    if waypoints:
        params["waypoints"] = "|".join(spot.name for spot in waypoints)

    return f"{base_url}&{urllib.parse.urlencode(params)}"


def build_distance_matrix(spots: list[Spot]) -> list[list[float]]:
    """Build a distance matrix between spots, returning a 2D list."""
    n = len(spots)
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                coordinates_i = spots[i].coordinates
                coordinates_j = spots[j].coordinates
                if coordinates_i is None or coordinates_j is None:
                    raise ValueError("all spots must have valid coordinates")
                matrix[i][j] = gps_distance_m(coordinates_i, coordinates_j)
    return matrix
