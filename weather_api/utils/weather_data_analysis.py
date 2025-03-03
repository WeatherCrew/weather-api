"""Module for analyzing weather data.

Provides functions to calculate annual and seasonal temperature means from a parsed .dly file for a specified time period.
"""
import pandas as pd


def preprocess_weather_data(data):
    """Transform parsed .dly data into a long-format DataFrame.

    Args:
        data (pd.DataFrame): Parsed data with columns ["ID", "YEAR", "MONTH", "ELEMENT", "DAY_1", ..., "DAY_31"].

    Returns:
        pd.DataFrame: Long-format DataFrame with columns ["ID", "YEAR", "MONTH", "ELEMENT", "DAY", "VALUE"].
    """
    melted = data.melt(
        id_vars=["ID", "YEAR", "MONTH", "ELEMENT"],
        value_vars=[f"DAY_{i}" for i in range(1, 32)],
        var_name="DAY",
        value_name="VALUE"
    ).dropna(subset=["VALUE"])

    melted["VALUE"] = melted["VALUE"] / 10.0
    return melted


def calculate_annual_means(preprocessed_data, start_year, end_year):
    """Calculate annual temperature means from preprocessed weather data.

    Args:
        preprocessed_data (pd.DataFrame): Long-format DataFrame from preprocess_weather_data.
        start_year (int): Start year for the analysis period.
        end_year (int): End year for the analysis period.

    Returns:
        pd.DataFrame: DataFrame with columns ["YEAR", "TMIN", "TMAX"].
    """
    # Filter data to include only the specified years
    annual_data = preprocessed_data[(preprocessed_data["YEAR"] >= start_year) & (preprocessed_data["YEAR"] <= end_year)]

    # Group data by 'YEAR' and 'ELEMENT' and calculate the mean 'VALUE' for each group
    annual_means = annual_data.groupby(["YEAR", "ELEMENT"])["VALUE"].mean().unstack()
    # Reset index to convert 'YEAR' from index back to a column
    annual_means = annual_means.reset_index()

    return annual_means


def calculate_seasonal_means(preprocessed_data, start_year, end_year, hemisphere):
    """Calculate seasonal temperature means from preprocessed weather data.

    Args:
        preprocessed_data (pd.DataFrame): Long-format DataFrame from preprocess_weather_data.
        start_year (int): Start year for the analysis period.
        end_year (int): End year for the analysis period.
        hemisphere (str): "N" for Northern, "S" for Southern hemisphere.

    Returns:
        pd.DataFrame: DataFrame with columns ["YEAR", "season", "TMIN", "TMAX"].
    """
    # Season mapping for Northern hemisphere
    season_map_north = {12: ("winter", 1), 1: ("winter", 0), 2: ("winter", 0),
                        3: ("spring", 0), 4: ("spring", 0), 5: ("spring", 0),
                        6: ("summer", 0), 7: ("summer", 0), 8: ("summer", 0),
                        9: ("autumn", 0), 10: ("autumn", 0), 11: ("autumn", 0)}
    # Season mapping for Southern hemisphere
    season_map_south = {12: ("summer", 1), 1: ("summer", 0), 2: ("summer", 0),
                        3: ("autumn", 0), 4: ("autumn", 0), 5: ("autumn", 0),
                        6: ("winter", 0), 7: ("winter", 0), 8: ("winter", 0),
                        9: ("spring", 0), 10: ("spring", 0), 11: ("spring", 0)}

    season_map = season_map_south if hemisphere.upper() == "S" else season_map_north

    # Map each month to its corresponding season and year
    preprocessed_data["season"], preprocessed_data["year_offset"] = zip(
        *preprocessed_data["MONTH"].map(lambda m: season_map.get(m, (None, 0)))
    )
    preprocessed_data["season_year"] = preprocessed_data["YEAR"] + preprocessed_data["year_offset"]

    # Filter to requested seasonal years
    seasonal_data = preprocessed_data[(preprocessed_data["season_year"] >= start_year) &
                                      (preprocessed_data["season_year"] <= end_year)].copy()

    seasonal_means = seasonal_data.groupby(["season_year", "season", "ELEMENT"])["VALUE"].mean().unstack()
    seasonal_means = seasonal_means.reset_index().rename(columns={"season_year": "YEAR"})

    return seasonal_means
