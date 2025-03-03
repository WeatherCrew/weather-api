import pytest
from weather_api.utils.stations_loader import stations_cache

@pytest.fixture(autouse=True)
def mock_initialize_station_data(monkeypatch):
    """Mock the initialize_station_data function to return a predefined test station for testing."""
    def mock_data():
        return {"stations": {"TEST001": {"station_id": "TEST001", "latitude": 0, "longitude": 0, "name": "Test", "hemisphere": "N", "data_availability": {"first_year": 2000, "last_year": 2020}}}}
    monkeypatch.setattr("weather_api.utils.stations_loader.initialize_station_data", mock_data)
    stations_cache.clear()
    stations_cache.update(mock_data())