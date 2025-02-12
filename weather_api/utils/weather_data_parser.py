import pandas as pd

def parse_dly_file(file_content):
    """
        Parst den Inhalt einer .dly-Datei und extrahiert nur die Datensätze für TMIN und TMAX.

        Jeder Datensatz enthält:
          - ID: Stations-ID (Zeichen 1-11)
          - YEAR: Jahr (Zeichen 12-15)
          - MONTH: Monat (Zeichen 16-17)
          - ELEMENT: Messgröße (TMIN oder TMAX, Zeichen 18-21)
          - DAY_1 bis DAY_31: Tageswerte (je 5 Zeichen pro Tag, beginnend bei Spalte 22)

        Fehlende Werte (z. B. "-9999") werden als None gespeichert.

        Args:
            file_content (str): Inhalt der .dly-Datei als String.

        Returns:
            pd.DataFrame: DataFrame mit den Spalten ["ID", "YEAR", "MONTH", "ELEMENT", "DAY_1", ..., "DAY_31"].
        """
    # Spaltennamen definieren
    columns = ["ID", "YEAR", "MONTH", "ELEMENT"] + [f"DAY_{i}" for i in range(1, 32)]
    data = []

    # Wir interessieren uns nur für TMIN und TMAX
    valid_elements = {"TMIN", "TMAX"}

    # Für jeden Eintrag in der Datei
    for line in file_content.splitlines():
        # Sicherstellen, dass die Zeile lang genug ist
        # Für 31 Tage: Startindex für DAY_31 = 21 + (30 * 8) = 21 + 240 = 261, plus 5 Zeichen = 266 (besser etwas großzügiger prüfen)
        if len(line) < 269:
            continue  # Zeile überspringen, wenn zu kurz

        # Extrahiere das Element (Spalten 18-21)
        element = line[17:21].strip()
        if element not in valid_elements:
            continue

        station_id = line[0:11].strip()
        try:
            year = int(line[11:15].strip())
            month = int(line[15:17].strip())
        except ValueError:
            continue  # Überspringe Zeile, falls Jahr oder Monat nicht konvertiert werden können

        # Lese die 31 Tageswerte ein; jeder Tageswert befindet sich in einem 8-Zeichen-Block
        values = []
        for i in range(31):
            start = 21 + (i * 8)
            end = start + 5  # Die ersten 5 Zeichen enthalten den Wert
            value_str = line[start:end].strip()
            if value_str == "-9999" or value_str == "":
                values.append(None)
            else:
                try:
                    values.append(int(value_str))
                except ValueError:
                    values.append(None)

        data.append([station_id, year, month, element] + values)

    return pd.DataFrame(data, columns=columns)


"""
    # Kommentar fehlt noch
    columns = ["ID", "YEAR", "MONTH", "ELEMENT"] + [f"DAY_{i}" for i in range(1, 32)]
    data = []

    for line in file_content.splitlines():
        station_id = line[0:11].strip()
        year = int(line[11:15].strip())
        month = int(line[15:17].strip())
        element = line[17:21].strip()

        values = [
            int(line[21 + (i * 8):26 + (i * 8)].strip()) if line[21 + (i * 8):26 + (i * 8)].strip() != "-9999" else None
            for i in range(31)
        ]
        data.append([station_id, year, month, element] + values)

    return pd.DataFrame(data, columns=columns)
"""