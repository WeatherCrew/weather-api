import time
import pytest
import requests
from weather_api.utils.weather_data_downloader import download_dly_file

def simulated_slow_response(*args, **kwargs):
    time.sleep(6)
    raise requests.exceptions.Timeout("Simulated timeout")

def test_download_dly_file(monkeypatch):
    # ersetzt requests.get durch simulated_slow_response
    monkeypatch.setattr("weather_api.utils.weather_data_downloader.requests.get", simulated_slow_response)

    with pytest.raises(TimeoutError):
        download_dly_file("test_station")
