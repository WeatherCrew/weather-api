import requests

def download_dly_file(station_id):
    # Kommentar fehlt noch
    # try / except fehlt noch

    base_url = "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/all/"
    file_url = f"{base_url}{station_id}.dly"

    try:
        response = requests.get(file_url, timeout=5) # Timeout nach 5 Sekunden, gemäß Anforderung
        response.raise_for_status()
        return response.text
    except requests.exceptions.Timeout:
        raise TimeoutError(f"Timeout: Download of file from {file_url} took more then 5 seconds.")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to download file from {file_url}: {e}")
