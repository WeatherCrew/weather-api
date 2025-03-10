"""Module for parsing weather data from .dly files.

Provides a function to parse weather data from .dly files for a given time period and extract TMIN and TMAX records
into a DataFrame.
"""
import pandas as pd
from weather_api.utils.weather_data_downloader import download_dly_file


def parse_dly_file(file_content, start_year, end_year):
    """Parse the content of a .dly file to extract TMIN and TMAX records between start_year - 1 and end_year.

    Processes the file content line by line, extracting station ID, year, month and daily values for TMIN and TMAX.
    Each record includes:
        - ID: Station ID (characters 1-11).
        - YEAR: Year (characters 12-15).
        - MONTH: Month (characters 16-17).
        - ELEMENT: Measurement type (TMIN and TMAX, characters 18-21).
        - DAY_1 to DAY_31: Daily values (5 characters per day, starting at character 22).

    Missing values (e.g. -9999) are stored as None.

    Args:
        file_content (str): Content of the .dly file as a string.
        start_year (int): First year of the analysis period.
        end_year (int): Last year of the analysis period.

    Returns:
        pd.DataFrame: DataFrame with columns ["ID", "YEAR", "MONTH", "ELEMENT", "DAY_1", ..., "DAY_31"].
    """
    # Define columns for the DataFrame
    columns = ["ID", "YEAR", "MONTH", "ELEMENT"] + [f"DAY_{i}" for i in range(1, 32)]
    data = []
    valid_elements = {"TMIN", "TMAX"}
    # Include the previous year for seasonal overlap
    min_year = start_year - 1

    # Parse each line in the file content
    for line in file_content.splitlines():
        # Skip lines shorter than 269 characters
        if len(line) < 269:
            continue

        # Extract element type and skip if not TMIN or TMAX
        element = line[17:21].strip()
        if element not in valid_elements:
            continue

        try:
            year = int(line[11:15].strip())
            if year < min_year or year > end_year:
                continue
            month = int(line[15:17].strip())
        except ValueError:
            continue # Skip line if year or month cannot be converted to integers

        station_id = line[0:11].strip()
        # values = []


        values = [None if line[21 + i * 8:26 + i * 8].strip() in ("-9999", "")
                  else int(line[21 + i * 8:26 + i * 8])
                  for i in range(31)]

        """
        # Parse 31 daily values (8-char blocks starting at character 22)
        for i in range(31):
            start = 21 + (i * 8)
            end = start + 5 # First 5 characters of each block are the value
            value_str = line[start:end].strip()
            if value_str == "-9999" or value_str == "":
                values.append(None)
            else:
                try:
                    values.append(int(value_str))
                except ValueError:
                    values.append(None)
        """

        data.append([station_id, year, month, element] + values)

    return pd.DataFrame(data, columns=columns)

from weather_api.utils.weather_data_downloader import download_dly_file

if __name__ == "__main__":
    file = download_dly_file("GME00129502")
    parsed_file = parse_dly_file(file, 1991, 2003)
    print(parsed_file)
