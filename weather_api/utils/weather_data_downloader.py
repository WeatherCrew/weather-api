"""
Download module for weather station data.

This module provides a function to download the .dly file for a given weather station.
"""

import requests

def download_dly_file(station_id):
    """Downloads the .dly file for a given weather station.

    The function constructs the file URL based on the station ID and attempts to download the corresponding .dly file.
    If the download takes longer than 5 seconds or another error occurs, an exception is raised.

    Args:
        station_id (str): The ID of the weather station. (e.g. "GME00129502").

    Returns:
        str: The content of the downloaded .dly file as a string.

    Raises:
        TimeoutError: If the download takes longer than 5 seconds.
        RuntimeError: If the download fails for any other reason.
    """

    base_url = "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/all/"
    file_url = f"{base_url}{station_id}.dly"

    try:
        response = requests.get(file_url, timeout=5)
        response.raise_for_status()
        return response.text
    except requests.exceptions.Timeout:
        raise TimeoutError(f"Timeout: Download of file from {file_url} took more then 5 seconds.")
    except Exception as e:
        raise RuntimeError(f"Failed to download file from {file_url}: {e}")


if __name__ == "__main__":
    print(download_dly_file("ASN00001000"))
