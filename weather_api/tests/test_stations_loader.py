import pytest
from weather_api.utils.stations_loader import (load_stations, parse_inventory_file, get_common_availability,
                                               initialize_station_data)


def test_load_stations_valid_file(tmp_path):
    """Tests loading station data from a valid CSV file."""
    csv_content = (
        "GME00129502,48.0092,8.8189,649.0,,TUTTLINGEN,,,\n"
        "GME00129514,47.9558,8.7575,675.0,,TUTTLINGEN-MOHRINGEN,,,\n"
        "GME00129526,51.3356,8.9142,295.0,,TWISTETAL-MUHLHAUSEN,,,\n"
        "GME00129538,47.7719,9.1569,446.0,,UBERLINGEN/BODENSEE,,,\n"
        "GME00129550,53.7458,14.0694,1.0,,UECKERMUNDE,,,\n"
        "GME00129562,52.9428,10.5300,50.0,,UELZEN,,,\n"
        "GME00129574,49.5753,10.1928,308.0,,GOLLHOFEN,,,\n"
        "GME00129586,48.3844,9.9539,567.0,,ULM,,,\n"
        "GME00129598,52.1617,11.1767,162.0,,UMMENDORF,,,\n"
        "GME00129610,52.8514,10.2908,95.0,,UNTERLUSS,,,\n"
        "GME00129622,49.5942,11.0717,291.0,,UTTENREUTH,,,\n"
        "GME00129634,48.0458,8.4617,720.0,,VILLINGEN-SCHWENNINGEN,,,\n"
    )

    file = tmp_path / "ghcnd-stations.csv"
    file.write_text(csv_content)

    stations = load_stations(file)
    assert len(stations) == 12
    assert stations[0] == {
        "station_id": "GME00129502",
        "latitude": 48.0092,
        "longitude": 8.8189,
        "name": "TUTTLINGEN",
        "hemisphere": "N",
    }
    assert stations[5] == {
        "station_id": "GME00129562",
        "latitude": 52.9428,
        "longitude": 10.5300,
        "name": "UELZEN",
        "hemisphere": "N",
    }
    assert stations[11] == {
        "station_id": "GME00129634",
        "latitude": 48.0458,
        "longitude": 8.4617,
        "name": "VILLINGEN-SCHWENNINGEN",
        "hemisphere": "N",
    }


def test_load_stations_file_not_found():
    """Tests that load_stations raises FileNotFoundError for an invalid file path."""
    with pytest.raises(FileNotFoundError, match="File not found"):
        load_stations("invalid_file_path.csv")


def test_load_stations_incomplete_data(tmp_path):
    """Tests that load_stations raises an IndexError for an incomplete CSV file."""
    csv_content = "GME00129502,48.0092\n"
    file = tmp_path / "ghcnd-stations.csv"
    file.write_text(csv_content)

    with pytest.raises(IndexError):
        load_stations(file)


def test_parse_inventory_file_valid_file(tmp_path):
    """Tests parsing an inventory file with valid data."""
    inventory_content = (
        "GME00129502  48.0092    8.8189 TMAX 1991 2003\n"
        "GME00129502  48.0092    8.8189 TMIN 1991 2003\n"
        "GME00129502  48.0092    8.8189 PRCP 1888 2017\n"
        "GME00129502  48.0092    8.8189 SNWD 1979 2017\n"
        "GME00129514  47.9558    8.7575 TMAX 1981 1990\n"
        "GME00129514  47.9558    8.7575 TMIN 1981 1990\n"
        "GME00129514  47.9558    8.7575 PRCP 1981 2024\n"
        "GME00129514  47.9558    8.7575 SNWD 1981 2024\n"
        "GME00129526  51.3356    8.9142 TMAX 1998 2024\n"
        "GME00129526  51.3356    8.9142 TMIN 1998 2024\n"
        "GME00129526  51.3356    8.9142 PRCP 1931 2024\n"
        "GME00129526  51.3356    8.9142 SNWD 1979 2024\n"
    )
    file = tmp_path / "ghcnd-inventory.txt"
    file.write_text(inventory_content)

    inventory = parse_inventory_file(file)

    assert "GME00129502" in inventory
    assert inventory["GME00129502"]["TMAX"] == {"first_year": 1991, "last_year": 2003}
    assert inventory["GME00129502"]["TMIN"] == {"first_year": 1991, "last_year": 2003}

    assert "GME00129514" in inventory
    assert inventory["GME00129514"]["TMAX"] == {"first_year": 1981, "last_year": 1990}
    assert inventory["GME00129514"]["TMIN"] == {"first_year": 1981, "last_year": 1990}

    assert "GME00129526" in inventory
    assert inventory["GME00129526"]["TMAX"] == {"first_year": 1998, "last_year": 2024}
    assert inventory["GME00129526"]["TMIN"] == {"first_year": 1998, "last_year": 2024}

    assert "PRCP" not in inventory["GME00129502"]
    assert "SNWD" not in inventory["GME00129502"]


def test_parse_inventory_file_file_not_found():
    """Tests that parse_inventory_file raises FileNotFoundError for an invalid file path."""
    with pytest.raises(FileNotFoundError, match="File not found"):
        parse_inventory_file("invalid_file_path.txt")


def test_parse_inventory_file_ignore_non_tmin_tmax(tmp_path):
    """Tests that parse_inventory_file ignores elements other than TMIN and TMAX."""
    inventory_content = (
        "GME00129502  48.0092    8.8189 PRCP 1888 2017\n"
        "GME00129514  47.9558    8.7575 TMAX 1981 1990\n"
        "GME00129514  47.9558    8.7575 TMIN 1981 1990\n"
        "GME00129514  47.9558    8.7575 SNWD 1981 2024\n"
        "GME00129526  51.3356    8.9142 TMAX 1998 2024\n"
        "GME00129526  51.3356    8.9142 TMIN 1998 2024\n"
        "GME00129526  51.3356    8.9142 PRCP 1931 2024\n"
    )
    file = tmp_path / "ghcnd-inventory.txt"
    file.write_text(inventory_content)

    inventory = parse_inventory_file(file)

    assert "GME00129502" not in inventory

    assert "GME00129514" in inventory
    assert inventory["GME00129514"]["TMAX"] == {"first_year": 1981, "last_year": 1990}
    assert inventory["GME00129514"]["TMIN"] == {"first_year": 1981, "last_year": 1990}
    assert "SNWD" not in inventory["GME00129514"]

    assert "GME00129526" in inventory
    assert inventory["GME00129526"]["TMAX"] == {"first_year": 1998, "last_year": 2024}
    assert inventory["GME00129526"]["TMIN"] == {"first_year": 1998, "last_year": 2024}
    assert "PRCP" not in inventory["GME00129526"]


def test_parse_invalid_inventory_file(tmp_path):
    """Tests that parse_inventory_file raises an error for a too-short line."""
    inventory_content = "GME00129502  48.0092    8.8189 TMAX 1991\n" # last_year missing
    file = tmp_path / "ghcnd-inventory.txt"
    file.write_text(inventory_content)

    with pytest.raises(ValueError, match="invalid literal for int"):
        parse_inventory_file(file)


def test_get_common_availability_both_tmin_tmax():
    """Tests get_common_availability with the same TMIN and TMAX data."""
    inventory = {
        "GME00129502": {
            "TMIN": {"first_year": 1991, "last_year": 2003},
            "TMAX": {"first_year": 1991, "last_year": 2003},
        }
    }
    availability = get_common_availability(inventory, "GME00129502")
    assert availability == {"first_year": 1991, "last_year": 2003}


def test_get_common_availability_missing_station():
    """Tests get_common_availability with a missing station ID."""
    inventory = {}
    availability = get_common_availability(inventory, "GME00129502")
    assert availability == {"first_year": None, "last_year": None}


def test_get_common_availability_only_tmin():
    """Tests get_common_availability with only TMIN data."""
    inventory = {
        "GME00129502": {
            "TMIN": {"first_year": 1991, "last_year": 2003},
            "TMAX": None,
        }
    }
    availability = get_common_availability(inventory, "GME00129310")
    assert availability == {"first_year": None, "last_year": None}


def test_get_common_availability_invalid_range():
    """Tests get_common_availability for the case that first_year > last_year."""
    inventory = {
        "GME00129310": {
            "TMIN": {"first_year": 1995, "last_year": 1948},
            "TMAX": {"first_year": 1995, "last_year": 1948},
        }
    }
    availability = get_common_availability(inventory, "GME00129310")
    assert availability == {"first_year": None, "last_year": None}


def test_get_common_availability_same_year():
    """Tests get_common_availability for the case that first_year == last_year."""
    inventory = {
        "GME00129502": {
            "TMIN": {"first_year": 2000, "last_year": 2000},
            "TMAX": {"first_year": 2000, "last_year": 2000},
        }
    }
    availability = get_common_availability(inventory, "GME00129502")
    assert availability == {"first_year": 2000, "last_year": 2000}


def test_initialize_station_valid_data(tmp_path, monkeypatch):
    """Tests successful initialization of station data."""
    stations_content = (
        "GME00129502,48.0092,8.8189,649.0,,TUTTLINGEN,,,\n"
        "GME00129514,47.9558,8.7575,675.0,,TUTTLINGEN-MOHRINGEN,,,\n"
    )
    stations_file = tmp_path / "ghcnd-stations.csv"
    stations_file.write_text(stations_content)

    inventory_content = (
        "GME00129502  48.0092    8.8189 TMAX 1991 2003\n"
        "GME00129502  48.0092    8.8189 TMIN 1991 2003\n"
        "GME00129514  47.9558    8.7575 TMAX 1981 1990\n"
        "GME00129514  47.9558    8.7575 TMIN 1981 1990\n"
    )
    inventory_file = tmp_path / "ghcnd-inventory.txt"
    inventory_file.write_text(inventory_content)

    def mock_load_stations():
        return load_stations(stations_file)

    def mock_parse_inventory_file():
        return parse_inventory_file(inventory_file)

    monkeypatch.setattr("weather_api.utils.stations_loader.load_stations", mock_load_stations)
    monkeypatch.setattr("weather_api.utils.stations_loader.parse_inventory_file", mock_parse_inventory_file)

    result = initialize_station_data()

    assert "stations" in result
    stations = result["stations"]
    assert len(stations) == 2
    assert "GME00129502" in stations
    assert stations["GME00129502"] == {
        "station_id": "GME00129502",
        "latitude": 48.0092,
        "longitude": 8.8189,
        "name": "TUTTLINGEN",
        "hemisphere": "N",
        "data_availability": {"first_year": 1991, "last_year": 2003}
    }
    assert "GME00129514" in stations
    assert stations["GME00129514"]["data_availability"] == {"first_year": 1981, "last_year": 1990}
    # noch andere Prüfung


def test_initialize_station_data_file_not_found(tmp_path, monkeypatch):
    """Tests that initialize_station_data raises FileNotFoundError if files are missing."""
    stations_content = "GME00129502,48.0092,8.8189,649.0,,TUTTLINGEN,,,\n"
    stations_file = tmp_path / "ghcnd-stations.csv"
    stations_file.write_text(stations_content)

    def mock_load_stations():
        return load_stations(stations_file)

    def mock_parse_inventory_file():
        raise FileNotFoundError("File not found")

    monkeypatch.setattr("weather_api.utils.stations_loader.load_stations", mock_load_stations)
    monkeypatch.setattr("weather_api.utils.stations_loader.parse_inventory_file", mock_parse_inventory_file)

    with pytest.raises(FileNotFoundError, match="File not found"):
        initialize_station_data()


def test_initialize_station_data_missing_inventory(tmp_path, monkeypatch):
    """Tests that stations without inventory data get default availability."""
    stations_content = (
        "GME00129502,48.0092,8.8189,649.0,,TUTTLINGEN,,,\n"
        "GME00129514,47.9558,8.7575,675.0,,TUTTLINGEN-MOHRINGEN,,,\n"
    )
    stations_file = tmp_path / "ghcnd-stations.csv"
    stations_file.write_text(stations_content)

    inventory_content = (
        "GME00129502  48.0092    8.8189 TMAX 1991 2003\n"
        "GME00129502  48.0092    8.8189 TMIN 1991 2003\n"
    )
    inventory_file = tmp_path / "ghcnd-inventory.txt"
    inventory_file.write_text(inventory_content)

    def mock_load_stations():
        return load_stations(stations_file)

    def mock_parse_inventory_file():
        return parse_inventory_file(inventory_file)

    monkeypatch.setattr("weather_api.utils.stations_loader.load_stations", mock_load_stations)
    monkeypatch.setattr("weather_api.utils.stations_loader.parse_inventory_file", mock_parse_inventory_file)

    result = initialize_station_data()
    stations = result["stations"]
    assert "GME00129502" in stations
    assert stations["GME00129502"]["data_availability"] == {"first_year": 1991, "last_year": 2003}
    assert "GME00129514" in stations
    assert stations["GME00129514"]["data_availability"] == {"first_year": None, "last_year": None}