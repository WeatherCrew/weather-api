"""Tests for the weather data analysis functions.

Values for the assertions were calculated manually.
"""
import os
import pytest
from weather_api.utils.weather_data_parser import parse_dly_file
from weather_api.utils.weather_data_analysis import preprocess_weather_data, calculate_annual_means, \
    calculate_seasonal_means


TEST_DATA_PATH_1 = os.path.join(os.path.dirname(__file__), "data", "GME00129502.dly.txt")


@pytest.fixture
def real_dly_content():
    """Fixture to load the real GME00129502.dly.txt file content."""
    with open(TEST_DATA_PATH_1, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def parsed_data(real_dly_content):
    """Fixture to parse the real .dly file for 1991-2003."""
    return parse_dly_file(real_dly_content, start_year=1991, end_year=2003)


@pytest.fixture
def preprocessed_data(parsed_data):
    """Fixture to preprocess the parsed data."""
    return preprocess_weather_data(parsed_data)


def test_preprocess_weather_data(preprocessed_data):
    """Test that preprocess_weather_data correctly transforms data into long format."""
    expected_columns = ["ID", "YEAR", "MONTH", "ELEMENT", "DAY", "VALUE"]
    assert list(preprocessed_data.columns) == expected_columns

    assert set(preprocessed_data["ELEMENT"].unique()) == {"TMIN", "TMAX"}

    # test first available value for GME00129502 (data availability starts in february 1991)
    jan_1991_tmax_day1 = preprocessed_data[(preprocessed_data["YEAR"] == 1991) &
                                           (preprocessed_data["MONTH"] == 2) &
                                           (preprocessed_data["DAY"] == "DAY_1") &
                                           (preprocessed_data["ELEMENT"] == "TMAX")]
    assert jan_1991_tmax_day1["VALUE"].iloc[0] == -4.0


def test_calculate_annual_means_1991(preprocessed_data):
    """Test annual means for TMIN and TMAX in 1991."""
    df = calculate_annual_means(preprocessed_data, start_year=1991, end_year=1991)

    assert list(df.columns) == ["YEAR", "TMAX", "TMIN"]
    assert df["YEAR"].iloc[0] == 1991

    tmin_mean = round(df["TMIN"].iloc[0], 1)
    tmax_mean = round(df["TMAX"].iloc[0], 1)
    assert tmin_mean == pytest.approx(2.8, abs=0.1)
    assert tmax_mean == pytest.approx(13.2, abs=0.1)


def test_calculate_annual_means_1995(preprocessed_data):
    """Test annual means for TMIN and TMAX in 1995."""
    df = calculate_annual_means(preprocessed_data, start_year=1992, end_year=1992)

    assert df["YEAR"].iloc[0] == 1992
    tmin_mean = round(df["TMIN"].iloc[0], 1)
    tmax_mean = round(df["TMAX"].iloc[0], 1)
    assert tmin_mean == pytest.approx(3.6, abs=0.1)
    assert tmax_mean == pytest.approx(13.0, abs=0.1)


def test_calculate_annual_means_2003(preprocessed_data):
    """Test annual means for TMIN and TMAX in 2003."""
    df = calculate_annual_means(preprocessed_data, start_year=2003, end_year=2003)

    assert df["YEAR"].iloc[0] == 2003
    tmin_mean = round(df["TMIN"].iloc[0], 1)
    tmax_mean = round(df["TMAX"].iloc[0], 1)
    assert tmin_mean == pytest.approx(2.8, abs=0.1)
    assert tmax_mean == pytest.approx(14.3, abs=0.1)


def test_calculate_seasonal_means_1991(preprocessed_data):
    """Test seasonal means for TMIN and TMAX in 1991 (Northern Hemisphere)."""
    df = calculate_seasonal_means(preprocessed_data, start_year=1991, end_year=1991, hemisphere="N")

    assert list(df.columns) == ["YEAR", "season", "TMAX", "TMIN"]

    # Winter 1991
    winter = df[(df["YEAR"] == 1991) & (df["season"] == "winter")]
    assert round(winter["TMIN"].iloc[0], 1) == pytest.approx(-9.4, abs=0.1)
    assert round(winter["TMAX"].iloc[0], 1) == pytest.approx(2.4, abs=0.1)

    # Summer 1991
    summer = df[(df["YEAR"] == 1991) & (df["season"] == "summer")]
    assert round(summer["TMIN"].iloc[0], 1) == pytest.approx(10.1, abs=0.1)
    assert round(summer["TMAX"].iloc[0], 1) == pytest.approx(22.4, abs=0.1)


def test_calculate_seasonal_means_1995(preprocessed_data):
    """Test seasonal means for TMIN and TMAX in 1995 (Northern Hemisphere)."""
    df = calculate_seasonal_means(preprocessed_data, start_year=1992, end_year=1992, hemisphere="N")

    # Winter 1992
    winter = df[(df["YEAR"] == 1992) & (df["season"] == "winter")]
    assert round(winter["TMIN"].iloc[0], 1) == pytest.approx(-5.0, abs=0.1)
    assert round(winter["TMAX"].iloc[0], 1) == pytest.approx(3.5, abs=0.1)

    # Summer 1992
    summer = df[(df["YEAR"] == 1992) & (df["season"] == "summer")]
    assert round(summer["TMIN"].iloc[0], 1) == pytest.approx(11.4, abs=0.1)
    assert round(summer["TMAX"].iloc[0], 1) == pytest.approx(22.5, abs=0.1)


def test_calculate_seasonal_means_2003(preprocessed_data):
    """Test seasonal means for TMIN and TMAX in 2003 (Northern Hemisphere)."""
    df = calculate_seasonal_means(preprocessed_data, start_year=2003, end_year=2003, hemisphere="N")

    # Winter 2003
    winter = df[(df["YEAR"] == 2003) & (df["season"] == "winter")]
    assert round(winter["TMIN"].iloc[0], 1) == pytest.approx(-4.3, abs=0.1)
    assert round(winter["TMAX"].iloc[0], 1) == pytest.approx(2.2, abs=0.1)

    # Summer 2003
    summer = df[(df["YEAR"] == 2003) & (df["season"] == "summer")]
    assert round(summer["TMIN"].iloc[0], 1) == pytest.approx(12.3, abs=0.1)
    assert round(summer["TMAX"].iloc[0], 1) == pytest.approx(26.9, abs=0.1)


TEST_DATA_PATH_2 = os.path.join(os.path.dirname(__file__), "data", "AR000087925.dly.txt")


# Fixtures for southern hemisphere station AR000087925
@pytest.fixture
def real_dly_content_2():
    """Fixture to load the real AR000087925.dly.txt file content."""
    with open(TEST_DATA_PATH_2, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def parsed_data_2(real_dly_content_2):
    """Fixture to parse the real .dly file for 1957."""
    return parse_dly_file(real_dly_content_2, start_year=1957, end_year=1957)


@pytest.fixture
def preprocessed_data_2(parsed_data_2):
    """Fixture to preprocess the parsed data."""
    return preprocess_weather_data(parsed_data_2)

def test_calculate_annual_means_1957(preprocessed_data_2):
    """Test annual means for TMIN and TMAX in 1957 (Southern Hemisphere)."""
    df = calculate_annual_means(preprocessed_data_2, start_year=1957, end_year=1957)

    assert list(df.columns) == ["YEAR", "TMAX", "TMIN"]
    assert df["YEAR"].iloc[0] == 1957

    tmin_mean = round(df["TMIN"].iloc[0], 1)
    tmax_mean = round(df["TMAX"].iloc[0], 1)
    assert tmin_mean == pytest.approx(1.8, abs=0.1)
    assert tmax_mean == pytest.approx(13.1, abs=0.1)


def test_calculate_seasonal_means_southern_hemisphere(preprocessed_data_2):
    """Test seasonal means for TMIN and TMAX in 1957 (Southern Hemisphere)."""
    df = calculate_seasonal_means(preprocessed_data_2, start_year=1957, end_year=1957, hemisphere="S")

    # Summer 1957
    summer = df[(df["YEAR"] == 1957) & (df["season"] == "summer")]
    assert round(summer["TMIN"].iloc[0], 1) == pytest.approx(6.0, abs=0.1)
    assert round(summer["TMAX"].iloc[0], 1) == pytest.approx(19.1, abs=0.1)

    # Autumn 1957
    autumn = df[(df["YEAR"] == 1957) & (df["season"] == "autumn")]
    assert round(autumn["TMIN"].iloc[0], 1) == pytest.approx(0.5, abs=0.1)
    assert round(autumn["TMAX"].iloc[0], 1) == pytest.approx(13.7, abs=0.1)

    # Winter 1957
    winter = df[(df["YEAR"] == 1957) & (df["season"] == "winter")]
    assert round(winter["TMIN"].iloc[0], 1) == pytest.approx(-2.2, abs=0.1)
    assert round(winter["TMAX"].iloc[0], 1) == pytest.approx(4.6, abs=0.1)

    # Winter 1957
    spring = df[(df["YEAR"] == 1957) & (df["season"] == "spring")]
    assert round(spring["TMIN"].iloc[0], 1) == pytest.approx(1.6, abs=0.1)
    assert round(spring["TMAX"].iloc[0], 1) == pytest.approx(13.0, abs=0.1)