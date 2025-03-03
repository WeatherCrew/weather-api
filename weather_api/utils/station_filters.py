"""Module for filtering weather stations based on location and temporal criteria.

Provides functions to filter station data by proximity to a reference point and data availability
for specified time periods, supporting queries in the weather analysis API.
"""
from weather_api.utils.stations_distance_calculation import haversine


def filter_stations(stations, latitude, longitude, radius, max_results, requested_start_year, requested_end_year):
    """Filter weather stations by distance and data availability.

    Calculates the distance from a reference point using the Haversine formula and filters stations within
    the specified radius and with data availability covering the requested time period.

    Args:
        stations (dict): Station data with station IDs as keys.
        latitude (float): Latitude of the reference point.
        longitude (float): Longitude of the reference point.
        radius (float): Maximum distance in kilometers.
        max_results (int): Maximum number of results to return.
        requested_start_year (int): Required start year of data availability.
        requested_end_year (int): Required end year of data availability.

    Returns:
        list[dict]: Sorted list of stations (by distance, up to max_results), each with keys "station_id", "latitude",
                    "longitude", "name", "hemisphere", "data_availability" and "distance".
    """
    results = []

    for station in stations.values():
        distance = haversine(latitude, longitude, station["latitude"], station["longitude"])
        if distance <= radius:
            availability = station["data_availability"]
            if availability["first_year"] and availability["last_year"]:
                if availability["first_year"] <= requested_start_year and availability["last_year"] >= requested_end_year:
                    result_entry = {
                        **station, # Unpacks all key-value pairs for the station
                        "distance": round(distance, 2)
                    }
                    results.append(result_entry)

    return sorted(results, key=lambda x: x["distance"])[:max_results] # Sorts by distance and returns up to max_results