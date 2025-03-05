import os
import pytest
from rest_framework.test import APIClient
from weather_api.utils.stations_loader import stations_cache

TEST_DATA_PATH_2 = os.path.join(os.path.dirname(__file__), "data", "AR000087925.dly.txt")

pytestmark = pytest.mark.analysis_view_2


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
def dly_content_2():
    """Fixture to load AR000087925.dly.txt content (Southern Hemisphere)."""
    with open(TEST_DATA_PATH_2, "r", encoding="utf-8") as f:
        return f.read()

def test_station_analysis_view_southern_hemisphere_1957(client, monkeypatch, dly_content_2):
    """Test successful GET request for AR000087925 in 1957 (Southern Hemisphere)."""
    mock_cache = {
        "stations": {
            "AR000087925": {"station_id": "AR000087925", "hemisphere": "S"}
        }
    }
    monkeypatch.setattr("weather_api.utils.stations_loader.stations_cache", mock_cache)
    monkeypatch.setattr("weather_api.utils.weather_data_downloader.download_dly_file",
                        lambda x: dly_content_2 if x == "AR000087925" else "")

    response = client.get('/api/stations/analysis/',
                          {'station_id': 'AR000087925', 'start_year': 1957, 'end_year': 1957})

    assert response.status_code == 200, f"Failed with response: {response.json()}"
    data = response.json()
    assert data["years"][0]["year"] == 1957
    assert round(data["years"][0]["annual_means"]["tmin"], 1) == pytest.approx(1.8, abs=0.1)
    assert round(data["years"][0]["annual_means"]["tmax"], 1) == pytest.approx(13.1, abs=0.1)
    assert round(data["years"][0]["seasonal_means"]["winter"]["tmin"], 1) == pytest.approx(-2.2, abs=0.1)
    assert round(data["years"][0]["seasonal_means"]["summer"]["tmax"], 1) == pytest.approx(19.1, abs=0.1)