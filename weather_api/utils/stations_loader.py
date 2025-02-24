"""Module for loading and initializing weather station data.

This module provides functions to load station data from a CSV file and parse data availability from an inventory file,
and initializes a cached dictionary of station data with common availability periods for TMIN and TMAX elements. The
initialized data is stored in `stations_cache`for access across the weather API.
"""


def load_stations(file_path="weather_api/data/ghcnd-stations.csv"):
    """Load station data from a CSV file.

        Reads station information from a CSV file. The file is expected to have at least six comma-separated
        columns, where:
          - Column 0: Station ID.
          - Column 1: Latitude.
          - Column 2: Longitude.
          - Column 5: Station name.

        The hemisphere is determined based on the latitude (>= 0 means "N", otherwise "S").

        Args:
            file_path (str): Path to the CSV file containing station data.
                             Defaults to "weather_api/data/ghcnd-stations.csv".

        Returns:
            list[dict]: List of dictionaries, each representing a station with keys:
                "station_id", "latitude", "longitude", "name", and "hemisphere".

        Raises:
            FileNotFoundError: If the file is not found.
    """
    stations = []
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            for line in file:
                row = line.split(",")
                station_id = row[0].strip() # .strip() removes whitespaces
                latitude = float(row[1].strip())
                longitude = float(row[2].strip())
                name = row[5].strip()

                stations.append({
                    "station_id": station_id,
                    "latitude": latitude,
                    "longitude": longitude,
                    "name": name,
                    "hemisphere": "N" if latitude >= 0 else "S" # "N" for northern, "S" for southern hemisphere
                })
    except FileNotFoundError:
        raise FileNotFoundError("File not found")
    return stations


def parse_inventory_file(file_path="weather_api/data/ghcnd-inventory.txt"):
    """Parse the inventory file and extract data availability information.

        Extracts the following details for each record:
          - Station ID: characters 0-11.
          - Element (e.g., TMIN or TMAX): characters 31-35.
          - First year: characters 36-40.
          - Last year: characters 41-45.

        Only "TMIN" and "TMAX" elements are  stored in a nested dictionary per station.

        Args:
            file_path (str): Path to the inventory file.
                             Defaults to "weather_api/data/ghcnd-inventory.txt".

        Returns:
            dict: Station IDs mapped to dictionaries with "TMIN" and "TMAX" keys, each containing "first_year" and
            "last_year" vakues.

        Raises:
            FileNotFoundError: If the file is not found.
        """
    inventory = {}
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            for line in file:
                station_id = line[0:11].strip()
                element = line[31:35].strip()
                first_year = int(line[36:40].strip())
                last_year = int(line[41:45].strip())

                if element in ["TMIN", "TMAX"]:
                    if station_id not in inventory:
                        inventory[station_id] = {"TMIN": None, "TMAX": None}
                    inventory[station_id][element] = {"first_year": first_year, "last_year": last_year}
    except FileNotFoundError:
        raise FileNotFoundError("File not found")
    return inventory


def get_common_availability(inventory, station_id):
    """Compute common data availability for a station based on TMIN and TMAX.

        Determines the overlapping data availability period by:
            - Taking the maximum of TMIN and TMAX first years.
            - Taking the minimum of TMIN and TMAX last years.

        Returns a default {first_year: None, last_year: None} if the station is not found or the range is invalid.

        Args:
            inventory (dict): Inventory data for stations.
            station_id (str): ID of the station to check.

        Returns:
            dict: Dictionary "first_year" and "last_year" keys for the common availability period.

        Raises:
            Noch error handling hinzufügen??
        """
    default_availability = {"first_year": None, "last_year": None}

    if station_id not in inventory:
        return default_availability

    station_data = inventory[station_id]
    tmin = station_data.get("TMIN") # kann man das ersetzen?
    tmax = station_data.get("TMAX")

    if tmin and tmax:
        # Find overlapping time period: latest start and earliest end
        first_year = max(tmin["first_year"], tmax["first_year"])
        last_year = min(tmin["last_year"], tmax["last_year"])

        if first_year <= last_year:
            return {"first_year": first_year, "last_year": last_year}

    return default_availability


def initialize_station_data():
    """Initialize station data by combining station and inventory information.

        Loads station data from a CSV file and availability data from an inventory file, calculates common TMIN/TMAX
        availability for each station, and stores the result in a dictionary keyed by station ID.

        Returns:
            dict: Station IDs mapped to dictionaries with station information and data availability.

        Raises:
            Noch error handling hinzufügen??
    """
    # Load raw station data
    stations_list = load_stations("weather_api/data/ghcnd-stations.csv")
    inventory = parse_inventory_file("weather_api/data/ghcnd-inventory.txt")
    stations = {}

    # Combine station metadata with availability data
    for station in stations_list:
        station_id = station["station_id"]
        availability = get_common_availability(inventory, station_id)
        station["data_availability"] = availability
        stations[station_id] = station

    print("Station data initialized")
    return {"stations": stations}


stations_cache = {}
"""dict: Cache for weather station data loaded by `initialize_station_data()`."""