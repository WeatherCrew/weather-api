import pytest
from weather_api.utils.stations_distance_calculation import haversine


def test_haversine_standard():
    """Test the distance between two well-known cities with tolerance."""
    assert haversine(52.5200, 13.4050, 48.8566, 2.3522) == pytest.approx(878.84, rel=0.01)

def test_haversine_northern_hemisphere():
    """Test points in the Northern Hemisphere."""
    assert round(haversine(52.52, 13.405, 48.8566, 2.3522), 2) > 0

def test_haversine_southern_hemisphere():
    """Test points in the Southern Hemisphere."""
    assert round(haversine(-25.47, -52.90, -30.0, -55.0), 2) > 0

def test_haversine_same_point():
    """Test the distance between the same coordinates (should be 0.0)."""
    assert haversine(52.5200, 13.4050, 52.5200, 13.4050) == 0.0

def test_haversine_poles():
    """Test the distance from the North Pole to the South Pole."""
    assert round(haversine(90, 0, -90, 0), 2) == 20015.09

def test_haversine_invalid_inputs():
    """Test that haversine raises RuntimeError for invalid inputs."""
    with pytest.raises(RuntimeError, match="Failed to calculate distance"):
        haversine("invalid", 13.4050, 48.8566, 2.3522)

    with pytest.raises(RuntimeError, match="Failed to calculate distance"):
        haversine(None, 13.4050, 48.8566, 2.3522)
