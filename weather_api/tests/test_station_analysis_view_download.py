import os
import pytest
from rest_framework.test import APIClient
from weather_api.utils.stations_loader import stations_cache

TEST_DATA_PATH_1 = os.path.join(os.path.dirname(__file__), "data", "GME00129502.dly.txt")

pytestmark = pytest.mark.analysis_view_3


@pytest.fixture(autouse=True)
def reset_stations_cache():
    """Fixture to reset stations_cache before each test to ensure isolation."""
    stations_cache.clear()
    stations_cache.update({"stations": {}})
    yield
    stations_cache.clear()


@pytest.fixture
def client():
    """Fixture providing an API client for testing."""
    return APIClient()


@pytest.fixture
def dly_content_1():
    """Fixture to load GME00129502.dly.txt content (Northern Hemisphere)."""
    with open(TEST_DATA_PATH_1, "r", encoding="utf-8") as f:
        return f.read()


def test_station_analysis_view_timeout(client, monkeypatch):
    """Test GET request with download timeout."""
    mock_cache = {
        "stations": {
            "GME00129502": {"station_id": "GME00129502", "hemisphere": "N"}
        }
    }
    monkeypatch.setattr("weather_api.utils.stations_loader.stations_cache", mock_cache)

    def mock_download_dly_file(station_id):
        if station_id == "GME00129502":
            raise TimeoutError("Download timeout")
        return "dummy_content"

    monkeypatch.setattr("weather_api.utils.weather_data_downloader.download_dly_file", mock_download_dly_file)

    response = client.get('/api/stations/analysis/',
                          {'station_id': 'GME00129502', 'start_year': 1991, 'end_year': 1991})
    assert response.status_code == 504, f"Failed with response: {response.json()}"
    assert "timeout" in response.json()["error"].lower()