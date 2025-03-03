import pytest
from weather_api.utils.station_filters import filter_stations


def test_filter_stations_within_radius():
    """Test filtering stations within a specified radius and time period."""
    stations = {
        "GME00129502": {
            "station_id": "GME00129502",
            "latitude": 48.0092,
            "longitude": 8.8189,
            "name": "TUTTLINGEN",
            "hemisphere": "N",
            "data_availability": {"first_year": 1991, "last_year": 2003}
        },
        "GME00129634": {
            "station_id": "GME00129634",
            "latitude": 48.0458,
            "longitude": 8.4617,
            "name": "VILLINGEN-SCHWENNINGEN",
            "hemisphere": "N",
            "data_availability": {"first_year": 1947, "last_year": 2024}
        }
    }
    result = filter_stations(stations, 48.0, 8.8, 50, 2, 2000, 2024)
    assert len(result) == 1
    assert result[0]["station_id"] == "GME00129634"
    assert result[0]["distance"] == pytest.approx(25.67, rel=0.01)
    assert "latitude" in result[0]
    assert "longitude" in result[0]
    assert "name" in result[0]
    assert "hemisphere" in result[0]
    assert "data_availability" in result[0]


def test_filter_stations_max_results():
    """Test limiting the number of returned stations to max_results."""
    stations = {
        "GME00129502": {
            "station_id": "GME00129502",
            "latitude": 48.0092,
            "longitude": 8.8189,
            "name": "TUTTLINGEN",
            "hemisphere": "N",
            "data_availability": {"first_year": 1991, "last_year": 2003}
        },
        "GME00129514": {
            "station_id": "GME00129514",
            "latitude": 47.9558,
            "longitude": 8.7575,
            "name": "TUTTLINGEN-MOHRINGEN",
            "hemisphere": "N",
            "data_availability": {"first_year": 1981, "last_year": 1990}
        },
        "GME00129634": {
            "station_id": "GME00129634",
            "latitude": 48.0458,
            "longitude": 8.4617,
            "name": "VILLINGEN-SCHWENNINGEN",
            "hemisphere": "N",
            "data_availability": {"first_year": 1947, "last_year": 2024}
        }
    }
    result = filter_stations(stations, 48, 8.8, 100, 1, 1995, 2000)
    assert len(result) == 1


def test_filter_stations_outside_radius():
    """Test when no stations are within the specified radius."""
    stations = {
        "GME00129502": {
            "station_id": "GME00129502",
            "latitude": 48.0092,
            "longitude": 8.8189,
            "name": "TUTTLINGEN",
            "hemisphere": "N",
            "data_availability": {"first_year": 1991, "last_year": 2003}
        },
        "GME00129514": {
            "station_id": "GME00129514",
            "latitude": 47.9558,
            "longitude": 8.7575,
            "name": "TUTTLINGEN-MOHRINGEN",
            "hemisphere": "N",
            "data_availability": {"first_year": 1981, "last_year": 1990}
        },
        "GME00129634": {
            "station_id": "GME00129634",
            "latitude": 48.0458,
            "longitude": 8.4617,
            "name": "VILLINGEN-SCHWENNINGEN",
            "hemisphere": "N",
            "data_availability": {"first_year": 1947, "last_year": 2024}
        }
    }
    result = filter_stations(stations, 52.0, 8.0, 50, 5, 1995, 2000)
    assert len(result) == 0


def test_filter_stations_time_period_mismatch():
    """Test when no stations match the requested time period."""
    stations = {
        "GME00129634": {
            "station_id": "GME00129634",
            "latitude": 48.0458,
            "longitude": 8.4617,
            "name": "VILLINGEN-SCHWENNINGEN",
            "hemisphere": "N",
            "data_availability": {"first_year": 1947, "last_year": 2024}
        }
    }
    result = filter_stations(stations, 48.0458, 8.4617, 50, 5, 1900, 2024)
    assert len(result) == 0


def test_filter_stations_empty_stations():
    """Test filtering with an empty stations dictionary."""
    stations = {}
    result = filter_stations(stations, 48.0, 8.9, 50, 5, 1900, 2024)
    assert len(result) == 0


def test_filter_stations_missing_availability():
    """Test when stations have no or incomplete availability data."""
    stations = {
        "GME00129310": {
            "station_id": "GME00129310",
            "latitude": 47.9403,
            "longitude": 8.1942,
            "name": "STATION1",
            "data_availability": {"first_year": None, "last_year": None}
        },
        "GME00129430": {
            "station_id": "GME00129430",
            "latitude": 47.9990,
            "longitude": 7.8421,
            "name": "STATION2",
            "data_availability": {"first_year": 1948, "last_year": None}
        }
    }
    result = filter_stations(stations, 47.9823, 8.8192, 50, 5, 1950, 1990)
    assert len(result) == 0


def test_filter_stations_sort_by_distance():
    """Test if stations are sorted by distance."""
    stations = {
        "GME00129502": {
            "station_id": "GME00129502",
            "latitude": 48.0092,
            "longitude": 8.8189,
            "name": "TUTTLINGEN",
            "hemisphere": "N",
            "data_availability": {"first_year": 1991, "last_year": 2003}
        },
        "GME00128002": {
            "station_id": "GME00128002",
            "latitude": 48.1819,
            "longitude": 8.6358,
            "name": "ROTTWEIL",
            "hemisphere": "N",
            "data_availability": {"first_year": 1957, "last_year": 2024}
        },
        "GME00129634": {
            "station_id": "GME00129634",
            "latitude": 48.0458,
            "longitude": 8.4617,
            "name": "VILLINGEN-SCHWENNINGEN",
            "hemisphere": "N",
            "data_availability": {"first_year": 1947, "last_year": 2024}
        }
    }
    result = filter_stations(stations, 48.0, 8.8, 100, 5, 1995, 2000)
    assert len(result) == 3
    assert result[0]["station_id"] == "GME00129502"
    assert result[1]["station_id"] == "GME00128002"
    assert result[2]["station_id"] == "GME00129634"
    assert result[0]["distance"] < result[1]["distance"]
    assert result[1]["distance"] < result[2]["distance"]
