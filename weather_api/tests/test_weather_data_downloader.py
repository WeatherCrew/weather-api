import pytest
import requests
from weather_api.utils.weather_data_downloader import download_dly_file


@pytest.fixture
def mock_response_success():
    """Fixture providing a mock response for a successful download."""

    class MockResponse:
        def __init__(self):
            self.text = "GME00129502200312TMAX   77  E  129  E   51  E   81  E   64  E   41  E   10  E  -36  E  -30  E   14  E   61  E   63  E   87  E   85  E   22  E    3  E    3  E   28  E    8  E   61  E   63  E    6  E  -20  E  -20  E    0  E    0  E   22  E   52  E   20  E    0  E    1  E\n"
        def raise_for_status(self):
            pass

    return MockResponse()


def test_download_dly_file_success(monkeypatch, mock_response_success):
    """Test successful download of a .dly file."""
    def mock_get(*args, **kwargs):
        return mock_response_success

    monkeypatch.setattr(requests, "get", mock_get)
    result = download_dly_file("GME00129502")

    assert isinstance(result, str)
    assert "GME00129502" in result
    assert "TMAX" in result


def test_download_dly_file_timeout(monkeypatch):
    """Test that a TimeoutError is raised if download exceeds 5 seconds."""
    def mock_get(*args, **kwargs):
        raise requests.exceptions.Timeout("Simulated timeout after 6 seconds")

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(TimeoutError, match=r"Timeout: Download of file from .* took more th[ae]n 5 seconds"):
        download_dly_file("GME00129502")


def test_download_dly_file_not_found(monkeypatch):
    """Test that a RuntimeError is raised for a non-existent station (HTTP 404)."""
    class MockResponse:
        def __init__(self):
            self.status_code = 404

        def raise_for_status(self):
            raise requests.exceptions.HTTPError("404 Client Error: Not Found")

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(RuntimeError, match=r"Failed to download file from .*404 Client Error"):
        download_dly_file("INVALID")


def test_download_dly_file_network_error(monkeypatch):
    """Test that a RuntimeError is raised for a general network error."""
    def mock_get(*args, **kwargs):
        raise requests.exceptions.ConnectionError("Network error")

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(RuntimeError, match=r"Failed to download file from .*Network error"):
        download_dly_file("GME00129502")


def test_download_dly_file_invalid_station_id(monkeypatch):
    """Test that a RuntimeError is raised for an invalid station_id like None."""

    def mock_get(*args, **kwargs):
        raise requests.exceptions.RequestException("Invalid request due to None station_id")

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(RuntimeError, match=r"Failed to download file from .*Invalid request"):
        download_dly_file(None)