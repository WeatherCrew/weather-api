# Analyse und Beschreibung der vorliegenden Daten

In der Datenquelle des *Daily Global Historical Climatology Network (GHCN)* stehen verschiedene Dateien zur Verfügung.
Zur Umsetzung der Kundenanforderungen werden sowohl Daten zu Wetterstationen (z. B. Längengrad, Breitengrad, Name) als auch Wetterdaten (insbesondere Minimal- und Maximaltemperaturen) benötigt.
Nachfolgend werden die dafür relevanten Daten beschrieben.

---

## Stationsdaten

Der Benutzer der Wetter-App gibt folgende Informationen ein:
- Längengrad
- Breitengrad
- Suchradius 
- Maximale Anzahl anzuzeigender Stationen
- Startjahr (Beginn der gewünschten Datenverfügbarkeit)
- Endjahr (Ende der gewünschten Datenverfügbarkeit)

Basierend auf diesen Eingaben sollen Wetterstationen identifiziert werden, die sich innerhalb des angegebenen Radius um den Standort befinden und für die Temperaturdaten im gewünschten Zeitraum verfügbar sind.

Für jede gefundene Wetterstation sollen folgende Informationen angezeigt werden:
- Name
- Stations-ID
- Längengrad
- Breitengrad
- Distanz zur angegebenen Position
- Zeitraum der Datenverfügbarkeit (Start- und Endjahr)

Die GHCN-Datenquelle bietet folgende Dateien mit Stationsinformationen:
- `ghcnd-inventory.txt`
- `ghcnd-stations.csv`
- `ghcnd-stations.txt`

Für die Umsetzung der Anforderungen werden folgende Dateien verwendet:
- `ghcnd-stations.csv` (https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.csv)
- `ghcnd-inventory.txt` (https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-inventory.txt)

### ghcnd-stations.csv

Die Datei dient dazu, Wetterstationen innerhalb des Suchradius zu lokalisieren. Sie enthält folgende Informationen:

| **Variable**   | **Columns (nur für .txt)** | **Type**     |
|-----------------|----------------------------|--------------|
| ID             | 1-11                       | Character    |
| LATITUDE       | 13-20                      | Real         |
| LONGITUDE      | 22-30                      | Real         |
| ELEVATION      | 32-37                      | Real         |
| STATE          | 39-40                      | Character    |
| NAME           | 42-71                      | Character    |
| GSN FLAG       | 73-75                      | Character    |
| HCN/CRN FLAG   | 77-79                      | Character    |
| WMO ID         | 81-85                      | Character    |

Beschreibung der Variablen:

- **ID**: Land (FIPS-Ländercode, Zeichen 1-2), Netzwerkcode (Zeichen 3), Stations-ID (Zeichen 4-11).
  - Siehe `ghcnd-countries.txt` für eine vollständige Liste der Ländercodes.
- **LATITUDE**: Breitengrad der Station.
- **LONGITUDE**: Längengrad der Station.
- **ELEVATION**: Höhe der Station (in Metern, fehlend = -999.9).
- **STATE**: Zweistelliger Code für US-Bundesstaaten.
  -  Siehe `ghcnd-states.txt` für eine Liste der Bundesstaats-/Provinz-/Territoriumscodes.
- **NAME**: Name der Station.
- **GSN FLAG**: Kennzeichnet Stationen des *GCOS Surface Network (GSN)*.
- **HCN/CRN FLAG**: Kennzeichnet Stationen des *U.S. Historical Climatology Network (HCN)* oder *U.S. Climate Reference Network (CRN)*.
- **WMO ID**: Nummer der *World Meteorological Organization (WMO)* für die Station (leer, falls nicht vorhanden).

Diese Datei (`ghcnd-stations.csv`) ist essenziell, da sie den Stationsnamen enthält. Allerdings enthält sie keine Informationen über den Zeitraum, für den Wetterdaten verfügbar sind.
Daher ist zusätzlich die Datei `ghcnd-inventory.txt` notwendig.

---

### ghcnd-inventory.txt

Neben Basisinformationen wie ID, Breiten- und Längengrad enthält diese Datei - im Gegensatz zu `ghcnd-stations.csv` - Informationen über den Zeitraum, für den Wetterdaten verfügbar sind.

| **Variable** | **Columns (nur für .txt)** | Type       |
|--------------|----------------------------|------------|
| ID           | 1-11                       | Character  |
| LATITUDE     | 13-20                      | Real       |
| LONGITUDE    | 22-30                      | Real       |
| ELEMENT      | 32-35                      | Character  |
| FIRSTYEAR    | 37-40                      | Integer    |
| LASTYEAR     | 42-45                      | Integer    |


Beschreibung der Variablen:

- **ID**: siehe `ghcnd-stations.txt/csv`
- **LATITUDE**: Breitengrad der Station.
- **LONGITUDE**: Längengrad der Station.
- **ELEMENT**: Es gibt verschiedene Elemente, darunter die folgenden 5 Kernelemente:
  - `PRCP`: Niederschlag (Zehntel mm)
  - `SNOW`: Schneefall (mm)
  - `SNWD`: Schneehöhe (mm)
  - `TMAX`: Maximaltemperatur (Zehntel Grad Celsius) → relevant für die Realisierung der Anforderungen des Kunden
  - `TMIN`: Minimaltemperatur (Zehntel Grad Celsius) → relevant für die Realisierung der Anforderungen des Kunden
- **FIRSTYEAR**: Erstes Jahr der Datenverfügbarkeit für das Element.
- **LASTYEAR**: Letztes Jahr der Datenverfügbarkeit für das Element.

---

## Wetterdaten zu einer Station:

Die GHCN-Datenquelle bietet verschiedene Dateien und Ordner mit Wetterdaten an:

- `all`: .dly-Dateien mit Daten pro Station.
- `by_station`: .csv.gz-Dateien pro Station.
- `by_year`: .csv.gz-Dateien pro Jahr für alle Stationen.
- `grid`: Jährliche Temperaturanomalien in einem 3,75° x 2,5° Raster.
- `gsn`: .dly-Dateien für GSN-Stationen.
- `hcn`: .dly-Dateien für HCN-Stationen.
- `isd`: (nicht näher spezifiziert)-

Eine Analyse der Dateien und Ordner ergab, dass nicht alle Dateien die in `ghcnd-inventory.txt` angegebenen Zeiträume enthalten oder vollständige Temperaturdaten (TMIN, TMAX) bereitstellen. Beispielsweise fehlen in `by_station`für die
Station `GME00129502` seit dem 26.01.2025 TMIN- und TMAX-Daten, obwohl sie am 25.01.2025 teilweise verfügbar waren, jedoch nicht für den gesamten angegebenen Zeitraum. Stand 08.03.2025 sind die Daten wieder verfügbar und nun auch für den gesamten Zeitraum abrufbar.

Da der Benutzer der Anwendung eine Wetterstation auswählt, für die er Wetterdaten angezeigt bekommen möchte, eignet sich das Abrufen der Wetterdaten für die angegebene Wetterstation und nicht für mehrere/alle Wetterstationen.
Daher ist der Ordner `all/` geeignet. Er enthält pro Station eine .dly-Datei mit vollständigen Daten über den gesamten Zeitraum.
Jede Zeile repräsentiert einen Monat, gekennzeichnet durch Element-Flags wie `TMIN`, `TMAX` oder `PRCP`. Für die Anforderungen des Kunden sind die Minimal- und Maximaltemperaturen (`TMIN`, `TMAX`) relevant.

Beispielzeile aus einer .dly-Datei:
`GME00129502 200211 TMAX  142  E  103  E  147  E   81  E   72  E   81  E   43  E   48  E   81  E   56  E  107  E  100  E  100  E   80  E   82  E   89  E  114  E   62  E   61  E   72  E   89  E   56  E   70  E   89  E   85  E   67  E   66  E   72  E   78  E   68  E-9999`

- **GME00129502**: Stations-ID
- **200211**: November 2002
- **TMAX**: Maximaltemperaturen
- **142**: 14,2 Grad Celsius 
- **-9999**: Keine Daten verfügbar (z. B. am 31. Tag im November)
- **E**: Source Flag, das angibt, woher die Daten stammen
  - E: *European Climate Assessment & Dataset*

--- 

## Quellen

- Datenquelle: https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/
- Wetterdaten pro Station: https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/{station_id}.dly
