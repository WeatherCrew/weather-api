import requests


def download_dly_file(station_id):
    # Kommentar fehlt noch
    # try / except fehlt noch

    base_url = "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/all/"
    file_url = f"{base_url}{station_id}.dly"

    response = requests.get(file_url)

    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to download file from {file_url}. Status code: {response.status_code}")