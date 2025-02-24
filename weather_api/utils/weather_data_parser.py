"""Module for parsing weather data from .dly files.

Provides a function to parse weather data from .dly files and extract TMIN and TMAX records into a DataFrame.
"""

import pandas as pd

def parse_dly_file(file_content):
    """Parse the content of a .dly file to extract TMIN adn TMAX records.

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

    Returns:
        pd.DataFrame: DataFrame with columns ["ID", "YEAR", "MONTH", "ELEMENT", "DAY_1", ..., "DAY_31"].
    """
    # Define columns for the DataFrame
    columns = ["ID", "YEAR", "MONTH", "ELEMENT"] + [f"DAY_{i}" for i in range(1, 32)]
    data = []

    valid_elements = {"TMIN", "TMAX"}

    # Parse each line in the file content
    for line in file_content.splitlines():
        # Skip lines shorter than 269 characters
        if len(line) < 269:
            continue

        # Extract element type and skip if not TMIN or TMAX
        element = line[17:21].strip()
        if element not in valid_elements:
            continue

        station_id = line[0:11].strip()
        try:
            year = int(line[11:15].strip())
            month = int(line[15:17].strip())
        except ValueError:
            continue  # Skip line if year or month cannot be converted to integers

        # Parse 31 daily values (8-char blocks starting at character 22)
        values = []
        for i in range(31):
            start = 21 + (i * 8)
            end = start + 5  # First 5 characters of each block are the value
            value_str = line[start:end].strip()
            if value_str == "-9999" or value_str == "":
                values.append(None)
            else:
                try:
                    values.append(int(value_str))
                except ValueError:
                    values.append(None)

        data.append([station_id, year, month, element] + values)

    return pd.DataFrame(data, columns=columns)
