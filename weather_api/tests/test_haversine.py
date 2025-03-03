import pytest
from weather_api.utils.stations_distance_calculation import haversine

def test_haversine_northern_hemisphere():
    """Test the distance between two points in the Northern Hemisphere."""
    distance = haversine(47.9823, 8.8192, 48.0594, 8.4641)
    assert distance == pytest.approx(27.78, rel=0.01)

def test_haversine_southern_hemisphere():
    """Test the distance between two points in the Southern Hemisphere."""
    distance = haversine(-8.7500, 116.2670, -8.5400, 118.6870)
    assert distance == pytest.approx(267, rel=0.01)

def test_haversine_northern_to_southern_hemisphere():
    """Test the distance between two points in different hemispheres."""
    distance = haversine(47.9823, 8.8192, -8.7500, 116.2670)
    assert distance == pytest.approx(12024, rel=0.01)

def test_haversine_same_point():
    """Test the distance between the same coordinates (should be 0.0)."""
    distance = haversine(47.9823, 8.8192, 47.9823, 8.8192)
    assert distance == 0.0

def test_haversine_boundary_values():
    """Test boundary values for latitude and longitude."""
    distance = haversine(90, 0, 90, 180)
    assert distance == pytest.approx(0, abs=0.01)

    distance = haversine(0, -180, 0, 180)
    assert distance == pytest.approx(0, abs=0.01)

def test_haversine_invalid_inputs():
    """Test error handling for invalid inputs."""
    with pytest.raises(RuntimeError, match="Failed to calculate distance"):
        haversine("invalid", 8.8192, 48.0594, 8.4641)
    with pytest.raises(RuntimeError, match="Failed to calculate distance"):
        haversine(47.9823, None, 48.0594, 8.4641)
    with pytest.raises(RuntimeError, match="Failed to calculate distance"):
        haversine(47.9823, 8.8192, "invalid", 8.4641)
    with pytest.raises(RuntimeError, match="Failed to calculate distance"):
        haversine(47.9823, 8.8192, 48.0594, None)
