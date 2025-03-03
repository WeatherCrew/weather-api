"""Module for building weather data responses.

Contains a function to build structured JSON responses with annual and seasonal temperature data for the weather
analysis API.
"""
import pandas as pd


def build_weather_data_response(annual_list, seasonal_list):
    """Build a structured JSON response with annual and seasonal temperature data.

    Combines annual and seasonal TMIN and TMAX data into a sorted list of yearly records, each containing annual means
    and seasonal means for winter, spring, summer, and autumn. Converts NaN values to None for JSON compatibility.

    Args:
        annual_list (list[dict]): List of annual data entries, each with keys "YEAR" (int), "TMIN" (float or None),
                                  and "TMAX" (float or None).
        seasonal_list (list[dict]): List of seasonal data entries, each with keys "YEAR" (int), "season" (str),
                                    "TMIN" (float or None), and "TMAX" (float or None).

    Returns:
        dict: A dictionary with a "years" key mapping to a sorted list of yearly dictionaries, each containing:
                - "year" (int): The year of the record.
                - "annual_means" (dict): Annual TMIN and TMAX means.
                - "seasonal_means" (dict): Seasonal TMIN and TMAX means for winter, spring, summer, and autumn.
    """
    expected_seasons = ["winter", "spring", "summer", "autumn"]
    years_dict = {}

    for row in annual_list:
        year = row["YEAR"]
        years_dict[year] = {
            "year": year,
            "annual_means": {
                "tmin": None if pd.isna(row["TMIN"]) else row["TMIN"],
                "tmax": None if pd.isna(row["TMAX"]) else row["TMAX"]
            },
            "seasonal_means": {season: {"tmin": None, "tmax": None} for season in expected_seasons}
        }

    for row in seasonal_list:
        year = row["YEAR"]
        season = row["season"]
        if year in years_dict and season in expected_seasons:
            years_dict[year]["seasonal_means"][season] = {
                "tmin": None if pd.isna(row["TMIN"]) else row["TMIN"],
                "tmax": None if pd.isna(row["TMAX"]) else row["TMAX"]
            }

    return {"years": [years_dict[y] for y in sorted(years_dict)]}
