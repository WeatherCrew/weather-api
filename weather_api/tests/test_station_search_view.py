import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from weather_api.utils.stations_loader import stations_cache


pytestmark = pytest.mark.search_view


@pytest.fixture(autouse=True)
def reset_stations_cache():
    stations_cache.clear()
    yield
    stations_cache.clear()


@pytest.fixture
def api_client():
    """Fixture providing an API client for testing."""
    return APIClient()


@pytest.fixture
def mock_stations_cache():
    """Fixture mocking the stations_cache with artificial station data."""
    stations_cache.clear()
    stations_cache["stations"] = {
        "STATION01": {
            "station_id": "STATION01",
            "latitude": 50.0,
            "longitude": 10.0,
            "name": "STATION01",
            "hemisphere": "N",
            "data_availability": {"first_year": 2010, "last_year": 2020}
        },
        "STATION02": {
            "station_id": "STATION02",
            "latitude": 51.0,
            "longitude": 11.0,
            "name": "STATION02",
            "hemisphere": "N",
            "data_availability": {"first_year": 2005, "last_year": 2024}
        },
        "STATION03": {
            "station_id": "STATION03",
            "latitude": -30.0,
            "longitude": 150.0,
            "name": "STATION03",
            "hemisphere": "S",
            "data_availability": {"first_year": 2015, "last_year": 2022}
        }
    }
    yield stations_cache
    stations_cache.clear()


def test_station_search_success(api_client, mock_stations_cache):
    """Test a successful weather station search."""
    url = reverse('station_search')
    params = {
        "latitude": 50.5,
        "longitude": 10.5,
        "radius": 1000,
        "max_results": 2,
        "start_year": 2012,
        "end_year": 2018
    }
    response = api_client.get(url, params)

    assert response.status_code == 200
    assert len(response.data) <= 2
    assert isinstance(response.data, list)

    for station in response.data:
        assert "station_id" in station
        assert "latitude" in station
        assert "longitude" in station
        assert "name" in station
        assert "distance" in station
        assert "data_availability" in station
        assert station["data_availability"]["first_year"] <= 2012
        assert station["data_availability"]["last_year"] >= 2018


def test_station_search_missing_params(api_client, mock_stations_cache):
    """Test response when required parameters are missing."""
    url = reverse('station_search')
    params = {
        "latitude": 50.5,
        "longitude": 10.5,
        # radius, max_results, start_year, end_year are missing
    }
    response = api_client.get(url, params)

    assert response.status_code == 400
    assert response.data == {"error": "Invalid parameters"}


def test_station_search_invalid_types(api_client, mock_stations_cache):
    """Test response when parameter types are invalid."""
    url = reverse('station_search')
    params = {
        "latitude": "invalid",
        "longitude": 10.5,
        "radius": 1000,
        "max_results": "two",  # Should be integer
        "start_year": 2012,
        "end_year": 2018
    }
    response = api_client.get(url, params)

    assert response.status_code == 400
    assert response.data == {"error": "Invalid parameters"}


def test_station_search_empty_cache(api_client):
    """Test response when stations_cache is empty."""
    # Wir setzen den Cache explizit auf leer:
    stations_cache["stations"] = {}
    url = reverse('station_search')
    params = {
        "latitude": 50.5,
        "longitude": 10.5,
        "radius": 1000,
        "max_results": 2,
        "start_year": 2012,
        "end_year": 2018
    }
    response = api_client.get(url, params)

    assert response.status_code == 500
    assert response.data == {"error": "Stations data not loaded"}

def test_station_search_no_results(api_client, mock_stations_cache):
    """Test response when no stations are found within the radius."""
    url = reverse('station_search')
    params = {
        "latitude": 0.0,
        "longitude": 0.0,
        "radius": 10,
        "max_results": 2,
        "start_year": 2012,
        "end_year": 2018
    }
    response = api_client.get(url, params)

    assert response.status_code == 200
    assert response.data == []


def test_station_search_radius_filter(api_client, mock_stations_cache):
    """Test if the radius filter works correctly."""
    url = reverse('station_search')
    params = {
        "latitude": 50.0,
        "longitude": 10.0,
        "radius": 100,
        "max_results": 5,
        "start_year": 2010,
        "end_year": 2020
    }
    response = api_client.get(url, params)

    assert response.status_code == 200
    assert len(response.data) > 0
    for station in response.data:
        assert station["distance"] <= 100


def test_station_search_time_filter(api_client, mock_stations_cache):
    """Test if the time period filter works correctly."""
    url = reverse('station_search')
    params = {
        "latitude": 50.5,
        "longitude": 10.5,
        "radius": 1000,
        "max_results": 5,
        "start_year": 2021,
        "end_year": 2024
    }
    response = api_client.get(url, params)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["station_id"] == "STATION02"
