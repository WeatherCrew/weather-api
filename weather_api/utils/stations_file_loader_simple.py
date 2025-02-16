from weather_api.utils.stations_distance_calculation import haversine


def load_stations(file_path="weather_api/data/ghcnd-stations.csv"):
    """Load station data from a CSV file.

        Reads station information from a CSV file. The file is expected to have at least six comma-separated
        columns, where:
          - Column 0 contains the station ID.
          - Column 1 contains the latitude.
          - Column 2 contains the longitude.
          - Column 5 contains the station name.

        The hemisphere is determined based on the latitude (>= 0 means "N", otherwise "S").

        Args:
            file_path (str): The path to the CSV file containing station data.
                             Defaults to "weather_api/data/ghcnd-stations.csv".

        Returns:
            list[dict]: A list of dictionaries, each representing a station with keys:
                "station_id", "latitude", "longitude", "name", and "hemisphere".

        Raises:
            FileNotFoundError: If the file is not found.
    """


    stations = []
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            for line in file:
                row = line.split(",")
                station_id = row[0].strip()
                latitude = float(row[1].strip())
                longitude = float(row[2].strip())
                name = row[5].strip()

                stations.append({
                    "station_id": station_id,
                    "latitude": latitude,
                    "longitude": longitude,
                    "name": name,
                    "hemisphere": "N" if latitude >= 0 else "S"
                })
    except FileNotFoundError:
        print("File not found")
    return stations


def parse_inventory_file(file_path="weather_api/data/ghcnd-inventory.txt"):
    """Parse the inventory file and extract data availability information.

        Reads a fixed-width formatted inventory file and extracts the following details for each record:
          - Station ID from characters 0 to 11.
          - Element (e.g., TMIN or TMAX) from characters 31 to 35.
          - First year from characters 36 to 40.
          - Last year from characters 41 to 45.

        Only the elements "TMIN" and "TMAX" are considered. For each station, the data is stored in a dictionary
        with keys "TMIN" and "TMAX", each holding a dictionary with "first_year" and "last_year".

        Args:
            file_path (str): The path to the inventory file.
                             Defaults to "weather_api/data/ghcnd-inventory.txt".

        Returns:
            dict: A dictionary where each key is a station ID and the value is another dictionary with keys "TMIN"
                  and "TMAX", each containing a dictionary with the keys "first_year" and "last_year".

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
        print("File not found")
    return inventory


def get_common_availability(inventory, station_id):
    """Compute the common data availability for a station based on TMIN and TMAX.

        For a given station, the common data availability is determined by taking:
          - The maximum of the first years for TMIN and TMAX.
          - The minimum of the last years for TMIN and TMAX.

        If the station is not found in the inventory or if the calculated range is invalid,
        a default dictionary with None values is returned.

        Args:
            inventory (dict): Dictionary containing inventory data for stations.
            station_id (str): The ID of the station to check.

        Returns:
            dict: A dictionary with keys "first_year" and "last_year" representing the common availability.

        Raises:
            Noch error handling hinzufügen??
        """
    default_availability = {"first_year": None, "last_year": None}

    if station_id not in inventory:
        return default_availability

    station_data = inventory[station_id]
    tmin = station_data.get("TMIN")
    tmax = station_data.get("TMAX")

    if tmin and tmax:
        first_year = max(tmin["first_year"], tmax["first_year"])
        last_year = min(tmin["last_year"], tmax["last_year"])

        if first_year <= last_year:
            return {"first_year": first_year, "last_year": last_year}

    return default_availability


def initialize_station_data():
    """Initialize station data by combining station and inventory information.

        Loads station data from a CSV file and inventory data from a text file. For each station,
        it calculates the common data availability (based on TMIN and TMAX) and appends this
        information to the station's data. The stations are then stored in a dictionary with
        station IDs as keys.

        Returns:
            dict: A dictionary where each key is a station ID and the corresponding value is a
                  dictionary containing station information including the computed data availability.

        Raises:
            Noch error handling hinzufügen??
    """

    stations_list = load_stations("weather_api/data/ghcnd-stations.csv")
    inventory = parse_inventory_file("weather_api/data/ghcnd-inventory.txt")
    stations = {}

    for station in stations_list:
        station_id = station["station_id"]
        availability = get_common_availability(inventory, station_id)
        station["data_availability"] = availability
        stations[station_id] = station

    print("Station data initialized")
    return stations


stations_cache = {
    "stations": initialize_station_data()
}


def filter_stations(stations, latitude, longitude, radius, max_results, requested_start_year, requested_end_year):
    """Filter stations based on proximity and data availability.

        Iterates through the stations, calculates the distance from the given geographic point
        (using the haversine formula), and filters out stations that are either outside the specified
        radius or do not have data availability covering the requested start and end years.

        Args:
            stations (dict): Dictionary of station data with station IDs as keys.
            latitude (float): Latitude of the reference point.
            longitude (float): Longitude of the reference point.
            radius (float): Maximum allowed distance (in kilometers) from the reference point.
            max_results (int): Maximum number of results to return.
            requested_start_year (int): The required start year of data availability.
            requested_end_year (int): The required end year of data availability.

        Returns:
            list[dict]: A sorted list of dictionaries representing the filtered stations. Each dictionary
                        includes a "distance" key (rounded to two decimal places). The list is sorted by
                        distance in ascending order and limited to max_results entries.

        Raises:
            error handling hinzufügen??
        """
    results = []
    for station in stations.values():
        distance = haversine(latitude, longitude, station["latitude"], station["longitude"])
        if distance <= radius:
            availability = station["data_availability"]
            if availability["first_year"] and availability["last_year"]:
                if availability["first_year"] <= requested_start_year and availability["last_year"] >= requested_end_year:
                    result_entry = {
                        **station,
                        "distance": round(distance, 2)
                    }
                    results.append(result_entry)
    return sorted(results, key=lambda x: x["distance"])[:max_results]
