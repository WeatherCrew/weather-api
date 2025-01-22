from weather_api.utils.distance_calculation import haversine

"""

csv file is currently available in the repo

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


def filter_stations(stations, latitude, longitude, radius, max_results):
    # Kommentar fehlt noch
    results = []
    for station in stations:
        distance = haversine(latitude, longitude, station["latitude"], station["longitude"])
        if distance <= radius:
            station["distance"] = round(distance, 2)
            results.append(station)

    return sorted(results, key=lambda x: x["distance"])[:max_results]