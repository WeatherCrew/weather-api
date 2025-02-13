import copy
from weather_api.utils.stations_distance_calculation import haversine

# global data structure
stations_cache = {
    "stations": None,
    "inventory": None
}

def initialize_station_data():
    global stations_cache
    stations_cache["stations"] = load_stations("weather_api/data/ghcnd-stations.csv")
    stations_cache["inventory"] = parse_inventory_file("weather_api/data/ghcnd-inventory.txt")
    print("Station data initialized")


"""

csv file is currently available in the repo because download is to slow (aprroxiamtely 180 seconds)

def download_stations_csv(url, output_path="weather/data/ghcnd-stations.csv"):
    # Kommentar fehlt noch
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_path, "wb") as file:
            file.write(response.content)
        print (f"File downloaded: {output_path}")
    else:
        raise Exception(f"Download failed: {response.status_code}")
        
        
"""


def load_stations(file_path="weather_api/data/ghcnd-stations.csv"):
    # Kommentar fehlt noch

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
                    "name": name
                })
    except FileNotFoundError:
        print("File not found")

    return stations


# added new function to parse inventory file
def parse_inventory_file(file_path="weather_api/data/ghcnd-inventory.txt"):
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
        print("Inventory file not found")
    return inventory


def get_common_availability(inventory, station_id):
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


def filter_stations(stations, latitude, longitude, radius, max_results, inventory, requested_start_year, requested_end_year):
    results = []
    for station in stations:
        distance = haversine(latitude, longitude, station["latitude"], station["longitude"])
        if distance <= radius:
            availability = get_common_availability(inventory, station["station_id"])
            if availability["first_year"] and availability["last_year"]:
                if availability["first_year"] <= requested_start_year and availability["last_year"] >= requested_end_year:
                    # Neues Dictionary basierend auf Original, ohne Original zu verändern
                    result_entry = {
                        **station,  # kopiert alle Werte aus Original
                        "distance": round(distance, 2),
                        "data_availability": availability
                    }
                    results.append(result_entry)
    return sorted(results, key=lambda x: x["distance"])[:max_results]


"""
old version with deepcopy --> unnecessary

def filter_stations(stations, latitude, longitude, radius, max_results, inventory, requested_start_year, requested_end_year):
    # verändern, sodass nicht immer eine deepcopy gemacht wird
    results = []
    for station in stations:
        distance = haversine(latitude, longitude, station["latitude"], station["longitude"])
        if distance <= radius:
            availability = get_common_availability(inventory, station["station_id"])

            if availability["first_year"] and availability["last_year"]:
                if availability["first_year"] <= requested_start_year and availability["last_year"] >= requested_end_year:
                    station_copy = copy.deepcopy(station)
                    station_copy["distance"] = round(distance, 2)
                    station_copy["data_availability"] = availability
                    results.append(station_copy)

    return sorted(results, key=lambda x: x["distance"])[:max_results]
"""

"""
            old version
            
            station["distance"] = round(distance, 2)

            # Datenverfügbarkeit prüfen
            availability = get_common_availability(inventory, station["station_id"])
            station["data_availability"] = availability

            results.append(station)
            

    return sorted(results, key=lambda x: x["distance"])[:max_results]
"""
