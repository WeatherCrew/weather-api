import pandas as pd

def calculate_annual_means(data, start_year, end_year):
    """"
    Docstring noch hinzufügen

    Muss hier dann auch der Dezember des Vorjahres eingebunden werden?
    """

    data_filtered = data[(data["YEAR"] >= start_year) & (data["YEAR"] <= end_year)]


    melted = data_filtered.melt(
        id_vars=["ID", "YEAR", "MONTH", "ELEMENT"],
        value_vars=[f"DAY_{i}" for i in range(1, 32)],
        var_name="DAY",
        value_name="VALUE"
    )

    # Entfernt Zeilen ohne gültigen Messwert
    melted = melted.dropna(subset=["VALUE"])

    melted["VALUE"] = melted["VALUE"] / 10.0

    # reset index kann man auch hier hinschreiben
    annual_means = melted.groupby(["YEAR", "ELEMENT"])["VALUE"].mean().unstack()

    annual_means = annual_means.reset_index()

    return annual_means

def assign_season(row, hemisphere):
    month = row["MONTH"]
    year = row["YEAR"]

    if hemisphere.upper() == "S":
        if month == 12:
            return year + 1, "summer"
        elif month in [1, 2]:
            return year, "summer"
        elif month in [3, 4, 5]:
            return year, "autumn"
        elif month in [6, 7, 8]:
            return year, "winter"
        elif month in [9, 10, 11]:
            return year, "spring"
    else:
        if month in [3, 4, 5]:
            return year, "spring"
        elif month in [6, 7, 8]:
            return year, "summer"
        elif month in [9, 10, 11]:
            return year, "autumn"
        elif month == 12:
            return year + 1, "winter"
        elif month in [1, 2]:
            return year, "winter"
    return year, None


def calculate_seasonal_means(data, start_year, end_year, hemisphere):
    """"
    Docstring noch hinzufügen
    """
    # Dezember des Vorjahres (start_year-1) für den Winter berücksichtigen
    data_filtered = data[(data["YEAR"] >= (start_year - 1)) & (data["YEAR"] <= end_year)]

    melted = data_filtered.melt(
        id_vars=["ID", "YEAR", "MONTH", "ELEMENT"],
        value_vars=[f"DAY_{i}" for i in range(1, 32)],
        var_name="DAY",
        value_name="VALUE"
    )

    melted = melted.dropna(subset=["VALUE"])
    melted["VALUE"] = melted["VALUE"] / 10.0

    melted[["season_year", "season"]] = melted.apply(lambda row: pd.Series(assign_season(row, hemisphere)), axis=1)

    melted = melted[(melted["season_year"] >= start_year) & (melted["season_year"] <= end_year)]

    seasonal_means = melted.groupby(["season_year", "season", "ELEMENT"])["VALUE"].mean().unstack()
    seasonal_means = seasonal_means.reset_index().rename(columns={"season_year": "YEAR"})

    return seasonal_means
