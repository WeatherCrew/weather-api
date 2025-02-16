"""
Module for geographic distance calculation using the Haversine formula.

This module provides a function to calculate the distance between two geographic coordinates (latitude and longitude)
using the Haversine formula.
"""

from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    """Calculates the distance between two geographic coordinates on earth.

    Args:
        lat1 (float): Latitude of the first point in decimal degrees (-90 to 90).
        lon1 (float): Longitude of the first point in decimal degrees (-180 to 180).
        lat2 (float): Latitude of the second point in decimal degrees (-90 to 90).
        lon2 (float): Longitude of the second point in decimal degrees (-180 to 180).

    Returns:
        float: The distance between the two points in kilometers.

    Raises:
        RuntimeError: If any unexpected error occurs.
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
