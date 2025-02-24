"""Module for calculating distances between locations on Earth.

This module provides a function to calculate the distance between two points using their latitude and longitude,
based on the Haversine formula.
"""
from math import radians, sin, cos, sqrt, atan2


def haversine(lat1, lon1, lat2, lon2):
    """Calculates the distance between two points on earth.

    Uses the Haversine formula to calculate the distance in kilometers based on latitude and longitude.

    Args:
        lat1 (float): Latitude of the first point (-90 to 90).
        lon1 (float): Longitude of the first point (-180 to 180).
        lat2 (float): Latitude of the second point (-90 to 90).
        lon2 (float): Longitude of the second point (-180 to 180).

    Returns:
        float: Distance between the two points in kilometers.

    Raises:
        RuntimeError: If the calculation fails unexpectedly.
    """
    try:
        R = 6371  # radius of earth in km
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
        c = (2 * atan2(sqrt(a), sqrt(1 - a)))  # atan2(sqrt(a), sqrt(1-a)) is equivalent
        return R * c
    except Exception as e:
        raise RuntimeError(f"Failed to calculate distance: {e}")
