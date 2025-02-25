"""Module for analyzing weather data.

Provides functions to calculate annual and seasonal temperature means from a parsed .dly file for a specified time period.
"""
import pandas as pd


def calculate_annual_means(data, start_year, end_year):
    """"Calculate annual temperature means from daily weather data.

    Filters weather data for the specified years, transforms it into a long format, calculates the mean TMIN and
    TMAX values per year and returns them in a structured DataFrame.

    Args:
        data(pd.DataFrame): Parsed weather data with columns ["ID", "YEAR", "MONTH", "ELEMENT", "DAY_1", ..., "DAY_31"].
        start_year (int): Start year for the analysis period.
        end_year (int): End year for the analysis period.

    Returns:
        pd.DataFrame: A DataFrame with columns ["YEAR", "TMIN", "TMAX"] containing annual means for TMIN and TMAX.
    """

    data_filtered = data[(data["YEAR"] >= start_year) & (data["YEAR"] <= end_year)]

    # Transform daily columns into a long format with one row per day and value
    melted = data_filtered.melt(
        id_vars=["ID", "YEAR", "MONTH", "ELEMENT"],
        value_vars=[f"DAY_{i}" for i in range(1, 32)],
        var_name="DAY",
        value_name="VALUE"
    )

    # Remove rows with missing measurements
    melted = melted.dropna(subset=["VALUE"])

    melted["VALUE"] = melted["VALUE"] / 10.0

    annual_means = (melted.groupby(["YEAR", "ELEMENT"])["VALUE"].mean().unstack())

    annual_means = annual_means.reset_index()

    return annual_means

def calculate_seasonal_means(data, start_year, end_year, hemisphere):
    data_filtered = data[(data["YEAR"] >= (start_year - 1)) & (data["YEAR"] <= end_year)].copy()

    # Melt nur einmal machen und speichern?
    melted = data_filtered.melt(
            id_vars=["ID", "YEAR", "MONTH", "ELEMENT"],
            value_vars=[f"DAY_{i}" for i in range(1, 32)],
            var_name="DAY",
            value_name="VALUE"
    ).dropna(subset=["VALUE"])

    melted["VALUE"] = melted["VALUE"] / 10.0

    # Vectorized season assignment
    season_map_north = {12: ("winter", 1), 1: ("winter", 0), 2: ("winter", 0),
                            3: ("spring", 0), 4: ("spring", 0), 5: ("spring", 0),
                            6: ("summer", 0), 7: ("summer", 0), 8: ("summer", 0),
                            9: ("autumn", 0), 10: ("autumn", 0), 11: ("autumn", 0)}
    season_map_south = {12: ("summer", 1), 1: ("summer", 0), 2: ("summer", 0),
                            3: ("autumn", 0), 4: ("autumn", 0), 5: ("autumn", 0),
                            6: ("winter", 0), 7: ("winter", 0), 8: ("winter", 0),
                            9: ("spring", 0), 10: ("spring", 0), 11: ("spring", 0)}

    season_map = season_map_south if hemisphere.upper() == "S" else season_map_north
    melted["season"], melted["year_offset"] = zip(*melted["MONTH"].map(lambda m: season_map.get(m, (None, 0))))
    melted["season_year"] = melted["YEAR"] + melted["year_offset"]

    melted = melted[(melted["season_year"] >= start_year) & (melted["season_year"] <= end_year)]

    seasonal_means = melted.groupby(["season_year", "season", "ELEMENT"])["VALUE"].mean().unstack()
    return seasonal_means.reset_index().rename(columns={"season_year": "YEAR"})

"""
def assign_season(row, hemisphere):
    Assign a season and year to a month based on the hemisphere.

        Determines the season (winter, spring, summer, autumn) and adjusts the year for cross-year seasons (e.g., Northern
        Hemisphere winter spanning December to February) based on the month and hemisphere.

        Args:
            row (pd.Series): A row from the DataFrame with "MONTH" (int) and "YEAR" (int) columns.
            hemisphere (str): Hemisphere of the station ("N" for Northern, "S" for Southern).

        Returns:
            tuple: A tuple of (season_year (int), season (str or None)) representing the adjusted year and season.
    """
"""
    month = row["MONTH"]
    year = row["YEAR"]

    if hemisphere.upper() == "S":
        # Southern Hemisphere
        if month == 12:
            return year + 1, "summer"
        elif month in [1, 2]:
            return year, "summer"
        elif month in [3, 4, 5]:
            return year, "autumn"
        elif month in [6, 7, 8]:
            return year, "winter"
        elif month in [9, 10, 11]:
            return year, "spring"
    else:
        # Northern Hemisphere
        if month in [3, 4, 5]:
            return year, "spring"
        elif month in [6, 7, 8]:
            return year, "summer"
        elif month in [9, 10, 11]:
            return year, "autumn"
        elif month == 12:
            return year + 1, "winter"
        elif month in [1, 2]:
            return year, "winter"
    return year, None


#def calculate_seasonal_means(data, start_year, end_year, hemisphere):
    Calculate seasonal temperature means from daily weather data.

    Filters weather data for the specified period (including December of the previous year for winter), transforms it into
    a long format, assigns seasons based on month and hemisphere, and computes mean TMIN and TMAX values per season and year.

    Args:
        data (pd.DataFrame): Parsed weather data with columns ["ID", "YEAR", "MONTH", "ELEMENT", "DAY_1", ..., "DAY_31"].
        start_year (int): First year of the analysis period.
        end_year (int): Last year of the analysis period.
        hemisphere (str): The hemisphere of the station ("N" for Northern, "S" for Southern).

    Returns:
        pd.DataFrame: A DataFrame with columns ["YEAR", "season", "TMIN", "TMAX"] containing seasonal means.
    

    # Include December of the previous year for winter (northern hemisphere) or summer (southern hemisphere)
    data_filtered = data[(data["YEAR"] >= (start_year - 1)) & (data["YEAR"] <= end_year)]

    # Transform daily columns into a long format with one row per day and value
    melted = data_filtered.melt(
        id_vars=["ID", "YEAR", "MONTH", "ELEMENT"],
        value_vars=[f"DAY_{i}" for i in range(1, 32)],
        var_name="DAY",
        value_name="VALUE"
    )

    # Remove rows with missing measurements
    melted = melted.dropna(subset=["VALUE"])

    melted["VALUE"] = melted["VALUE"] / 10.0

    # Assign season and adjusted year based on month and hemisphere
    melted[["season_year", "season"]] = melted.apply(lambda row: pd.Series(assign_season(row, hemisphere)), axis=1)

    # Filter to the specified year range after season assignment
    melted = melted[(melted["season_year"] >= start_year) & (melted["season_year"] <= end_year)]

    #
    seasonal_means = melted.groupby(["season_year", "season", "ELEMENT"])["VALUE"].mean().unstack()
    # Rename season_year to YEAR
    seasonal_means = seasonal_means.reset_index().rename(columns={"season_year": "YEAR"})

    return seasonal_means
"""