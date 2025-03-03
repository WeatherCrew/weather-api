from weather_api.utils.weather_data_response_builder import build_weather_data_response


def test_build_weather_data_response_full_data():
    """Test building a response with complete annual and seasonal data."""
    annual_list = [
        {'YEAR': 1995, 'TMAX': 12.56986301369863, 'TMIN': 3.163013698630137},
        {'YEAR': 1996, 'TMAX': 11.229234972677595, 'TMIN': 2.1040983606557377}
    ]
    seasonal_list = [
        {'YEAR': 1995, 'season': 'winter', 'TMAX': 4.634444444444445, 'TMIN': -2.5444444444444443},
        {'YEAR': 1995, 'season': 'spring', 'TMAX': 11.890217391304349, 'TMIN': 1.6445652173913046},
        {'YEAR': 1995, 'season': 'summer', 'TMAX': 21.532608695652176, 'TMIN': 10.677173913043477},
        {'YEAR': 1995, 'season': 'autumn', 'TMAX': 13.1, 'TMIN': 3.587912087912088},
        {'YEAR': 1996, 'season': 'winter', 'TMAX': 1.7648351648351648, 'TMIN': -4.728571428571429},
        {'YEAR': 1996, 'season': 'spring', 'TMAX': 11.856521739130434, 'TMIN': 1.481521739130435},
        {'YEAR': 1996, 'season': 'summer', 'TMAX': 20.75108695652174, 'TMIN': 9.582608695652175},
        {'YEAR': 1996, 'season': 'autumn', 'TMAX': 11.072527472527472, 'TMIN': 2.758241758241758},
    ]
    result = build_weather_data_response(annual_list, seasonal_list)

    assert "years" in result
    assert len(result["years"]) == 2
    assert result["years"][0]["year"] == 1995
    assert result["years"][0]["annual_means"] == {"tmin": 3.163013698630137, "tmax": 12.56986301369863}
    assert result["years"][0]["seasonal_means"] == {
        "winter": {"tmin": -2.5444444444444443, "tmax": 4.634444444444445},
        "spring": {"tmin": 1.6445652173913046, "tmax": 11.890217391304349},
        "summer": {"tmin": 10.677173913043477, "tmax": 21.532608695652176},
        "autumn": {"tmin": 3.587912087912088, "tmax": 13.1}
    }
    assert result["years"][1]["year"] == 1996
    assert result["years"][1]["annual_means"] == {"tmin": 2.1040983606557377, "tmax": 11.229234972677595}
    assert result["years"][1]["seasonal_means"] == {
        "winter": {"tmin": -4.728571428571429, "tmax": 1.7648351648351648},
        "spring": {"tmin": 1.481521739130435, "tmax": 11.856521739130434},
        "summer": {"tmin": 9.582608695652175, "tmax": 20.75108695652174},
        "autumn": {"tmin": 2.758241758241758, "tmax": 11.072527472527472}
    }


def test_build_weather_data_response_missing_values():
    """Test handling of NaN values in annual and seasonal data."""
    annual_list = [
        {'YEAR': 1995, 'TMAX': float("nan"), 'TMIN': 3.163013698630137},
    ]
    seasonal_list = [
        {'YEAR': 1995, 'season': 'winter', 'TMAX': 4.634444444444445, 'TMIN': -2.5444444444444443},
        {'YEAR': 1995, 'season': 'spring', 'TMAX': float("nan"), 'TMIN': 1.6445652173913046},
        {'YEAR': 1995, 'season': 'summer', 'TMAX': 21.532608695652176, 'TMIN': 10.677173913043477},
        {'YEAR': 1995, 'season': 'autumn', 'TMAX': 13.1, 'TMIN': float("nan")},

    ]
    result = build_weather_data_response(annual_list, seasonal_list)

    assert len(result["years"]) == 1
    assert result["years"][0]["year"] == 1995
    assert result["years"][0]["annual_means"] == {"tmin": 3.163013698630137, "tmax": None}
    assert result["years"][0]["seasonal_means"]["winter"] == {"tmin": -2.5444444444444443, "tmax": 4.634444444444445}
    assert result["years"][0]["seasonal_means"]["spring"] == {"tmin": 1.6445652173913046, "tmax": None}
    assert result["years"][0]["seasonal_means"]["summer"] == {"tmin": 10.677173913043477, "tmax": 21.532608695652176}
    assert result["years"][0]["seasonal_means"]["autumn"] == {"tmin": None, "tmax": 13.1}


def test_build_weather_data_response_empty_lists():
    """Test building a response with empty input lists."""
    annual_list = []
    seasonal_list = []
    result = build_weather_data_response(annual_list, seasonal_list)

    assert len(result["years"]) == 0


def test_build_weather_data_response_partial_seasons():
    """Test building a response with incomplete seasonal data."""
    annual_list = [
        {'YEAR': 1995, 'TMAX': 12.56986301369863, 'TMIN': 3.163013698630137}
    ]
    seasonal_list = [
        {'YEAR': 1995, 'season': 'summer', 'TMAX': 21.532608695652176, 'TMIN': 10.677173913043477},
        {'YEAR': 1995, 'season': 'autumn', 'TMAX': 13.1, 'TMIN': 3.587912087912088}
    ]
    result = build_weather_data_response(annual_list, seasonal_list)

    assert len(result["years"]) == 1
    assert result["years"][0]["year"] == 1995
    assert result["years"][0]["annual_means"] == {"tmin": 3.163013698630137, "tmax": 12.56986301369863}
    assert result["years"][0]["seasonal_means"]["winter"] == {"tmin": None, "tmax": None}
    assert result["years"][0]["seasonal_means"]["spring"] == {"tmin": None, "tmax": None}
    assert result["years"][0]["seasonal_means"]["summer"] == {"tmin": 10.677173913043477, "tmax": 21.532608695652176}
    assert result["years"][0]["seasonal_means"]["autumn"] == {"tmin": 3.587912087912088, "tmax": 13.1}


def test_build_weather_data_response_sorting():
    """Test that years are sorted in ascending order."""
    annual_list = [
        {'YEAR': 2000, 'TMAX': 13.532240437158471, 'TMIN': 3.949453551912568},
        {'YEAR': 1999, 'TMAX': 12.69095890410959, 'TMIN': 3.341917808219178},
        {'YEAR': 1998, 'TMAX': 12.78821917808219, 'TMIN': 2.750684931506849}

    ]
    seasonal_list = [
        {'YEAR': 2000, 'season': 'winter', 'TMAX': 3.6868131868131866, 'TMIN': -3.1725274725274724},
        {'YEAR': 2000, 'season': 'summer', 'TMAX': 22.003260869565217, 'TMIN': 9.764130434782608},
        {'YEAR': 2000, 'season': 'spring', 'TMAX': 14.133695652173913, 'TMIN': 3.319565217391304},
        {'YEAR': 2000, 'season': 'autumn', 'TMAX': 13.45054945054945, 'TMIN': 4.99010989010989},
        {'YEAR': 1999, 'season': 'winter', 'TMAX': 3.1011111111111114, 'TMIN': -5.046666666666667},
        {'YEAR': 1999, 'season': 'summer', 'TMAX': 21.32282608695652, 'TMIN': 10.282608695652174},
        {'YEAR': 1999, 'season': 'spring', 'TMAX': 13.265217391304349, 'TMIN': 3.8630434782608694},
        {'YEAR': 1999, 'season': 'autumn', 'TMAX': 12.762637362637363, 'TMIN': 3.5824175824175826},
        {'YEAR': 1998, 'season': 'winter', 'TMAX': 5.348888888888888, 'TMIN': -3.1900000000000004},
        {'YEAR': 1998, 'season': 'summer', 'TMAX': 21.952173913043477, 'TMIN': 10.01304347826087},
        {'YEAR': 1998, 'season': 'spring', 'TMAX': 13.18586956521739, 'TMIN': 2.2467391304347823},
        {'YEAR': 1998, 'season': 'autumn', 'TMAX': 10.702197802197801, 'TMIN': 2.921978021978022}
    ]
    result = build_weather_data_response(annual_list, seasonal_list)

    assert len(result["years"]) == 3
    assert result["years"][0]["year"] == 1998
    assert result["years"][1]["year"] == 1999
    assert result["years"][2]["year"] == 2000
