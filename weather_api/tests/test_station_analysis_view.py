import os
import pytest
from rest_framework.test import APIClient
from weather_api.utils.stations_loader import stations_cache

TEST_DATA_PATH_1 = os.path.join(os.path.dirname(__file__), "data", "GME00129502.dly.txt")

pytestmark = pytest.mark.analysis_view


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


def test_station_analysis_view_success_1991(client, monkeypatch, dly_content_1):
    """Test successful GET request for GME00129502 in 1991."""
    mock_cache = {
        "stations": {
            "GME00129502": {"station_id": "GME00129502", "hemisphere": "N"}
        }
    }
    monkeypatch.setattr("weather_api.utils.stations_loader.stations_cache", mock_cache)
    monkeypatch.setattr("weather_api.utils.weather_data_downloader.download_dly_file",
                        lambda x: dly_content_1 if x == "GME00129502" else "")

    response = client.get('/api/stations/analysis/',
                          {'station_id': 'GME00129502', 'start_year': 1991, 'end_year': 1991})

    assert response.status_code == 200, f"Failed with response: {response.json()}"
    data = response.json()
    assert "years" in data
    assert len(data["years"]) == 1
    year_data = data["years"][0]
    assert year_data["year"] == 1991
    assert round(year_data["annual_means"]["tmin"], 1) == pytest.approx(2.8, abs=0.1)
    assert round(year_data["annual_means"]["tmax"], 1) == pytest.approx(13.2, abs=0.1)
    assert round(year_data["seasonal_means"]["winter"]["tmin"], 1) == pytest.approx(-9.4, abs=0.1)
    assert round(year_data["seasonal_means"]["summer"]["tmax"], 1) == pytest.approx(22.4, abs=0.1)


def test_station_analysis_view_success_1992(client, monkeypatch, dly_content_1):
    """Test successful GET request for GME00129502 in 1992."""
    mock_cache = {
        "stations": {
            "GME00129502": {"station_id": "GME00129502", "hemisphere": "N"}
        }
    }
    monkeypatch.setattr("weather_api.utils.stations_loader.stations_cache", mock_cache)
    monkeypatch.setattr("weather_api.utils.weather_data_downloader.download_dly_file",
                        lambda x: dly_content_1 if x == "GME00129502" else "")

    response = client.get('/api/stations/analysis/',
                          {'station_id': 'GME00129502', 'start_year': 1992, 'end_year': 1992})

    assert response.status_code == 200, f"Failed with response: {response.json()}"
    data = response.json()
    assert data["years"][0]["year"] == 1992
    assert round(data["years"][0]["annual_means"]["tmin"], 1) == pytest.approx(3.6, abs=0.1)
    assert round(data["years"][0]["annual_means"]["tmax"], 1) == pytest.approx(13.0, abs=0.1)
    assert round(data["years"][0]["seasonal_means"]["winter"]["tmin"], 1) == pytest.approx(-5.0, abs=0.1)
    assert round(data["years"][0]["seasonal_means"]["summer"]["tmax"], 1) == pytest.approx(22.5, abs=0.1)


def test_station_analysis_view_success_2003(client, monkeypatch, dly_content_1):
    """Test successful GET request for GME00129502 in 2003."""
    mock_cache = {
        "stations": {
            "GME00129502": {"station_id": "GME00129502", "hemisphere": "N"}
        }
    }
    monkeypatch.setattr("weather_api.utils.stations_loader.stations_cache", mock_cache)
    monkeypatch.setattr("weather_api.utils.weather_data_downloader.download_dly_file",
                        lambda x: dly_content_1 if x == "GME00129502" else "")

    response = client.get('/api/stations/analysis/',
                          {'station_id': 'GME00129502', 'start_year': 2003, 'end_year': 2003})

    assert response.status_code == 200, f"Failed with response: {response.json()}"
    data = response.json()
    assert data["years"][0]["year"] == 2003
    assert round(data["years"][0]["annual_means"]["tmin"], 1) == pytest.approx(2.8, abs=0.1)
    assert round(data["years"][0]["annual_means"]["tmax"], 1) == pytest.approx(14.3, abs=0.1)
    assert round(data["years"][0]["seasonal_means"]["winter"]["tmin"], 1) == pytest.approx(-4.3, abs=0.1)
    assert round(data["years"][0]["seasonal_means"]["summer"]["tmax"], 1) == pytest.approx(26.9, abs=0.1)


def test_station_analysis_view_missing_params(client, monkeypatch):
    """Test GET request with missing parameters."""
    mock_cache = {
        "stations": {
            "GME00129502": {"station_id": "GME00129502", "hemisphere": "N"}
        }
    }
    monkeypatch.setattr("weather_api.utils.stations_loader.stations_cache", mock_cache)
    monkeypatch.setattr("weather_api.utils.weather_data_downloader.download_dly_file",
                        lambda x: "dummy_content" if x == "GME00129502" else "")

    # Without station_id
    response = client.get('/api/stations/analysis/', {'start_year': 1991, 'end_year': 1991})
    assert response.status_code == 400, f"Failed with response: {response.json()}"
    assert response.json() == {"error": "Missing parameter(s)"}

    # Without start_year
    response = client.get('/api/stations/analysis/', {'station_id': 'GME00129502', 'end_year': 1991})
    assert response.status_code == 400, f"Failed with response: {response.json()}"
    assert response.json() == {"error": "Missing parameter(s)"}

    # Without end_year
    response = client.get('/api/stations/analysis/', {'station_id': 'GME00129502', 'start_year': 1991})
    assert response.status_code == 400, f"Failed with response: {response.json()}"
    assert response.json() == {"error": "Missing parameter(s)"}


def test_station_analysis_view_invalid_year_range(client, monkeypatch):
    """Test GET request with start_year > end_year."""
    mock_cache = {
        "stations": {
            "GME00129502": {"station_id": "GME00129502", "hemisphere": "N"}
        }
    }
    monkeypatch.setattr("weather_api.utils.stations_loader.stations_cache", mock_cache)
    monkeypatch.setattr("weather_api.utils.weather_data_downloader.download_dly_file",
                        lambda x: "dummy_content" if x == "GME00129502" else "")

    response = client.get('/api/stations/analysis/',
                          {'station_id': 'GME00129502', 'start_year': 1992, 'end_year': 1991})
    assert response.status_code == 400, f"Failed with response: {response.json()}"
    assert response.json() == ["start_year must <= end_year"]


def test_station_analysis_view_station_not_found(client, monkeypatch):
    """Test GET request with unknown station_id."""
    mock_cache = {
        "stations": {
            "GME00129502": {"station_id": "GME00129502", "hemisphere": "N"}
        }
    }
    monkeypatch.setattr("weather_api.utils.stations_loader.stations_cache", mock_cache)
    monkeypatch.setattr("weather_api.utils.weather_data_downloader.download_dly_file",
                        lambda x: "dummy_content" if x == "GME00129502" else "")

    response = client.get('/api/stations/analysis/',
                          {'station_id': 'UNKNOWN123', 'start_year': 1991, 'end_year': 1991})
    assert response.status_code == 404, f"Failed with response: {response.json()}"
    assert response.json() == {"error": "Station not found"}
