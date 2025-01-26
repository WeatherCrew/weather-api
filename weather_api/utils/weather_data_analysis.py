import pandas as pd

def calculate_annual_means(data, start_year, end_year):
    # Kommentar fehlt noch

    data_filtered = data[
        (data["ELEMENT"].isin(["TMIN", "TMAX"])) &
        (data["YEAR"] >= start_year) &
        (data["YEAR"] <= end_year)
    ]

    melted = data_filtered.melt(
        id_vars=["YEAR", "MONTH", "ELEMENT"],
        value_vars=[f"DAY_{i}" for i in range(1, 32)],
        var_name="DAY",
        value_name="VALUE"
    ).dropna(subset=["VALUE"])

    melted["VALUE"] = melted["VALUE"] / 10.0

    annual_means = melted.groupby(["YEAR", "ELEMENT"])["VALUE"].mean().unstack()
    return annual_means.reset_index()


def calculate_seasonal_means(data, start_year, end_year):
    # Kommentar fehlt noch
    seasons = {
        "spring": [3, 4, 5],
        "summer": [6, 7, 8],
        "autumn": [9, 10, 11],
        "winter": [12, 1, 2]
    }

    data_filtered = data[
        (data["ELEMENT"].isin(["TMIN", "TMAX"])) &
        (data["YEAR"] >= start_year - 1) &
        (data["YEAR"] <= end_year + 1)
    ]

    data_filtered.loc[data_filtered["MONTH"] == 12, "YEAR"] += 1

    melted = data_filtered.melt(
        id_vars=["ID", "YEAR", "MONTH", "ELEMENT"],
        value_vars=[f"DAY_{i}" for i in range(1, 32)],
        var_name="DAY",
        value_name="VALUE"
    ).dropna(subset=["VALUE"])

    melted["VALUE"] = melted["VALUE"] / 10.0

    seasonal_means = []
    for season, months in seasons.items():
        season_data = melted[melted["MONTH"].isin(months)]

        available_years = season_data["YEAR"].unique()
        relevant_years = range(start_year, end_year + 1)

        for year in relevant_years:
            if year not in available_years:
                continue
            mean_values = season_data[season_data["YEAR"] == year].groupby("ELEMENT")["VALUE"].mean().to_frame().T
            mean_values["YEAR"] = year
            mean_values["SEASON"] = season
            seasonal_means.append(mean_values)

    return pd.concat(seasonal_means).reset_index(drop=True)