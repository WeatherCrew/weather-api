def build_weather_data_response(annual_list, seasonal_list):
    expected_seasons = ["winter", "spring", "summer", "autumn"]
    years_dict = {}

    for row in annual_list:
        year = row["YEAR"]
        years_dict[year] = {
            "year": year,
            "annual_means": {
                "tmin": row["TMIN"],
                "tmax": row["TMAX"]
            },
            "seasonal_means": {season: {"tmin": None, "tmax": None} for season in expected_seasons}
        }

    for row in seasonal_list:
        year = row["YEAR"]
        season = row["season"]
        if year in years_dict and season in expected_seasons:
            years_dict[year]["seasonal_means"][season] = {
                "tmin": row["TMIN"],
                "tmax": row["TMAX"]
            }
    years = [years_dict[y] for y in sorted(years_dict)]

    return {"years": years}
