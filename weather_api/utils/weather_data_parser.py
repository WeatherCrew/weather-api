import pandas as pd

def parse_dly_file(file_content):
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