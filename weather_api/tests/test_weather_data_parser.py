import os
import pandas as pd
import pytest
from weather_api.utils.weather_data_parser import parse_dly_file


TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "GME00129502.dly.txt")


@pytest.fixture
def real_dly_content():
    """Fixture to load the real GME00129502.dly.txt file content."""
    with open(TEST_DATA_PATH, "r", encoding="utf-8") as f:
        return f.read()


def test_parse_dly_file_tmin_tmax_only(real_dly_content):
    """Test that only TMIN and TMAX records are extracted within 1991-2003."""
    df = parse_dly_file(real_dly_content, start_year=1991, end_year=2003)

    assert set(df["ELEMENT"].unique()) == {"TMIN", "TMAX"}

    assert "PRCP" not in df["ELEMENT"].values
    assert "SNWD" not in df["ELEMENT"].values

    expected_columns = ["ID", "YEAR", "MONTH", "ELEMENT"] + [f"DAY_{i}" for i in range(1, 32)]
    assert list(df.columns) == expected_columns

    assert df["YEAR"].min() >= 1991
    assert df["YEAR"].max() <= 2003


def test_parse_dly_file_year_range_1991_2003(real_dly_content):
    """Test that the year range (1991 - 2003) is correctly applied."""
    start_year = 1991
    end_year = 2003
    df = parse_dly_file(real_dly_content, start_year=start_year, end_year=end_year)

    assert df["YEAR"].min() == start_year  # 1991 because there is no data for 1990
    assert df["YEAR"].max() == end_year

    assert all(df["YEAR"] >= 1990)
    assert all(df["YEAR"] <= 2003)

    assert 1888 not in df["YEAR"].values


def test_parse_dly_file_missing_values_1991(real_dly_content):
    """Test that missing values (-9999) are correctly parsed as None for 1991."""
    df = parse_dly_file(real_dly_content, start_year=1991, end_year=1991)

    feb_1991_tmax = df[(df["YEAR"] == 1991) & (df["MONTH"] == 2) & (df["ELEMENT"] == "TMAX")]
    assert not feb_1991_tmax.empty
    assert pd.isna(feb_1991_tmax["DAY_29"].iloc[0])
    assert pd.isna(feb_1991_tmax["DAY_30"].iloc[0])
    assert pd.isna(feb_1991_tmax["DAY_31"].iloc[0])

    assert feb_1991_tmax["DAY_1"].iloc[0] == -40 # value from the file


def test_parse_dly_file_specific_data_2003(real_dly_content):
    """Test specific TMAX data parsing for January 2003."""
    df = parse_dly_file(real_dly_content, start_year=2003, end_year=2003)

    jan_2003_tmax = df[(df["YEAR"] == 2003) & (df["MONTH"] == 1) & (df["ELEMENT"] == "TMAX")]
    assert not jan_2003_tmax.empty
    assert jan_2003_tmax["DAY_1"].iloc[0] == 71
    assert jan_2003_tmax["DAY_2"].iloc[0] == 110
    assert jan_2003_tmax["DAY_3"].iloc[0] == 81

    assert jan_2003_tmax["DAY_31"].iloc[0] == -40


def test_parse_dly_file_before_tmin_tmax_range(real_dly_content):
    """Test that no TMIN/TMAX data is returned for years before 1991."""
    df = parse_dly_file(real_dly_content, start_year=1888, end_year=1990)

    assert df.empty
    expected_columns = ["ID", "YEAR", "MONTH", "ELEMENT"] + [f"DAY_{i}" for i in range(1, 32)]
    assert list(df.columns) == expected_columns


def test_parse_dly_file_after_tmin_tmax_range(real_dly_content):
    """Test that no TMIN/TMAX data is returned for years after 2003."""
    df = parse_dly_file(real_dly_content, start_year=2005, end_year=2010)

    assert df.empty
    expected_columns = ["ID", "YEAR", "MONTH", "ELEMENT"] + [f"DAY_{i}" for i in range(1, 32)]
    assert list(df.columns) == expected_columns

def test_parse_dly_file_no_data_for_1990(real_dly_content):
    """Test that no TMIN/TMAX data is returned for 1990 despite start_year - 1."""
    df = parse_dly_file(real_dly_content, start_year=1991, end_year=1991)
    assert 1990 not in df["YEAR"].values