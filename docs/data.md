# Analyse und Beschreibung der vorliegenden Daten

In der vorliegenden Datenquelle des Daily Global Historical Climatology Network (GHCN) sind verschiedene Dateien verfügbar. 
Um die Anforderungen des Kunden umzusetzen, werden einerseits Daten zu Wetterstationen (z. B. Längengrad, Breitengrad, Name etc.) 
und andererseits Wetterdaten (insbesondere Temperaturen) benötigt. Im Folgenden werden daher die für die Umsetzung des Projekts notwendigen Daten beschrieben.

---

## Stationsdaten

Der Benutzer der Wetter-App gibt folgende Daten ein: Geografische Länge, Breite, einen Suchradius und die maximale Anzahl der Stationen, die angezeigt werden sollen.
Basierend darauf sollen die Wetterstationen gefunden werden, die sich innerhalb des angegebenen Radius um den Standort des Benutzers befinden.

Der Benutzer möchte pro gefundener Station folgende Daten angezeigt bekommen:
- Name
- ... (muss noch durch den Kunden spezifiziert werden)

Grundsätzlich enthalten die folgenden, in der Datenquelle verfügbaren Dateien, Informationen zu Wetterstationen:
- `ghcnd-inventory.txt`
- `ghcnd-stations.csv`
- `ghcnd-stations.txt`

Um die Anforderungen des Kunden umzusetzen, werden die folgenden Dateien benötigt: 
- `ghcnd-stations.csv` (https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.csv)
- `ghcnd-inventory.txt` (https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-inventory.txt)

### ghcnd-stations.csv

Die Datei wird benötigt, um die Wetterstationen zu finden, die sich innerhalb des Radius um den angegebenen Standort befinden.
Die Datei enthält folgende Informationen zu den Wetterstationen:

| **Variable**   | **Columns (nur for .txt)** | **Type**     |
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


Informationen zu den Variablen:

- **ID**: Die ersten beiden Zeichen identifizieren das Land (FIPS-Ländercode), das dritte Zeichen ist ein Netzwerkcode, der das Stationsnummerierungssystem identifiziert, und die verbleibenden acht Zeichen enthalten die tatsächliche Stations-ID.
  - Siehe `ghcnd-countries.txt` für eine vollständige Liste der Ländercodes.
  - Siehe `ghcnd-states.txt` für eine Liste der Bundesstaats-/Provinz-/Territoriumscodes.
  
  **Netwerkcode-Werte**:
  - `0` = unspecified (station identified by up to eight alphanumeric characters)
  - `1` = Community Collaborative Rain, Hail, and Snow (CoCoRaHS) based identification number.  
  - `C` = U.S. Cooperative Network identification number (last six characters of the GHCN-Daily ID).  
  - `E` = Identification number used in the ECA&D non-blended dataset.  
  - `M` = World Meteorological Organization ID (last five characters of the GHCN-Daily ID).  
  - `N` = Identification number used in data supplied by a National Meteorological or Hydrological Center.  
  - `P` = "Pre-Coop" (an internal identifier assigned by NCEI for station records collected prior to the establishment of the U.S. Weather Bureau).  
  - `R` = U.S. Interagency Remote Automatic Weather Station (RAWS) identifier.  
  - `S` = U.S. Natural Resources Conservation Service SNOTEL station identifier.  
  - `W` = WBAN identification number (last five characters of the GHCN-Daily ID).

- **LATITUDE**: Breitengrad der Station (in Dezimalgrad).

- **LONGITUDE**: Längengrad der Station (in Dezimalgrad).

- **ELEVATION**: Höhe der Station (in Metern, fehlend = -999.9).

- **STATE**: Der zweistellige Bundesstaatscode für die Station (nur für US-Stationen).

- **NAME**

- **GSN FLAG**  
  A flag that indicates whether the station is part of the GCOS Surface Network (GSN).  
  - Blank = Non-GSN station or WMO Station number not available.  
  - GSN = GSN station.

- **HCN/CRN FLAG**  
  A flag that indicates whether the station is part of the U.S. Historical Climatology Network (HCN) or U.S. Climate Reference Network (CRN).  
  - Blank = Not a member of the U.S. Historical Climatology or U.S. Climate Reference Networks.  
  - HCN = U.S. Historical Climatology Network station.  
  - CRN = U.S. Climate Reference Network or U.S. Regional Climate Network Station.

- **WMO ID**  
  The World Meteorological Organization (WMO) number for the station. If the station has no WMO number (or one has not yet been matched to this station), the field is blank.

Diese Datei ist notwendig, da sie Informationen über den Namen der Station enthält. Sie enthält jedoch keine Informationen über den Zeitraum, für den Wetterdaten zu einer Station verfügbar sind.
Daher ist zusätzlich die Datei `ghcnd-inventory.txt` notwendig.

---

### ghcnd-inventory.txt

Die Datei enthält wie die Datei `ghcnd-stations.txt/csv` Informationen zu Wetterstationen, wie z. B. die ID, Länge und Breite.
Die Datei enthält ebenfalls Informationen zu Wetterstationen, wie z. B. die ID, Länge und Breite. Zusätzlich enthält sie 
Informationen über den Zeitraum, für den Wetterdaten verfügbar sind. Diese Informationen sind **nur** in dieser Datei verfügbar.

Die Datei enthält folgende Informationen zu den Wetterstationen:

| Variable   | Columns   | Type       |
|------------|-----------|------------|
| ID         | 1-11      | Character  |
| LATITUDE   | 13-20     | Real       |
| LONGITUDE  | 22-30     | Real       |
| ELEMENT    | 32-35     | Character  |
| FIRSTYEAR  | 37-40     | Integer    |
| LASTYEAR   | 42-45     | Integer    |


Informationen zu den Variablen:

- **ID**: siehe Beschreibung `ghcnd-stations.txt/csv`

- **LATITUDE**: Breitengrad der Station (in Dezimalgrad).

- **LONGITUDE**: Längengrad der Station (in Dezimalgrad).

- **ELEMENT**: Es gibt verschiedene Elemente, davon 5 Kernelemente:
  - `PRCP`: Niederschlag (1/10 mm)
  - `SNOW`: Schneefall (1/10 mm)
  - `SNWD`: Schneehöhe (1 mm)
  - `TMAX`: Maximaltemperatur (0.1 Grad Celsius) → relevant für die Realisierung der Anforderungen des Kunden
  - `TMIN`: Minimaltemperatur (0.1 Grad Celsius) → relevant für die Realisierung der Anforderungen des Kunden

- **FIRSTYEAR**: erstes Jahr in dem Daten für ein Element verfügbar sind.

- **LASTYEAR**: letztes Jahr in dem Daten für ein Element verfügbar sind.

---

## Wetterdaten zu einer Station:

Es sind verschiedene Dateien mit Wetterdaten verfügbar. Dazu zählen folgende Ordner und Dateien:
- `all`: Enthält .dly-Dateien. Pro Wetterstation gibt es eine .dly-Datei.
- `by_station`: Enthält .csv.gz-Dateien. Pro Wetterstation gibt es eine .csv.gz-Datei. Sie soll Wetterdaten für die gesamte Aufzeichnungszeit enthalten (dies ist jedoch nicht der Fall - dazu später mehr).
- `by_year`: Enthält .csv.gz-Dateien. Pro Jahr gibt es eine .csv.gz-Datei, die Wetterdaten für alle Wetterstationen enthält.
- `grid`: Enthält jährliche Temperaturabweichungen für verschiedene Regionen.
- `gsn`: Enthält .dly-Dateien für Wetterstationen aus dem GCOS Surface Network (GSN).
- `hcn`: Enthält .dly-Dateien für Wetterstationen aus dem U.S. Historical Climatology Network (HCN).
- `isd`: Enthält Wetterdaten aus dem Integrated Surface Database (ISD). (nochmal spezifizieren)

Bei einer genaueren Analyse stellte sich jedoch heraus, dass nicht alle Dateien auch tatsächlich Daten für den in der Datei `ghcnd-inventory.txt` angegebenen Zeitraum enthalten bzw. gar Daten zu Temperaturen enthalten.
So verfügt bspw. die Datei für die Wetterstation `GME00129502`  im Ordner `by_station/` nicht über Daten zu Minimal- und Maximaltemperaturen (Stand: 26.01.2025).
Am 25.01.2025 enthielt die Datei noch Daten Minimal- und Maximaltemperaturen, allerdings nicht für den gesamten Zeitraum, der in der Datei `ghcnd-inventory.txt` angegeben ist.

Da der Benutzer der Anwendung eine Wetterstation auswählt, für die er Wetterdaten angezeigt bekommen möchte, eignet sich das Abrufen der Wetterdaten für die angegebene Wetterstation und nicht für mehrere/alle Wetterstationen.
Daher ist der Ordner `all/` geeignet. Denn er enthält, wie eine Analyse zeigte, pro Wetterstation eine .dly-Datei, die Wetterdaten für den gesamten Zeitraum enthält.

Eine .dly-Datei enthält Daten einer Wetterstation, wobei jede Zeile einen Monat repräsentiert. Jede Zeile gibt durch ein Element-Flag (z. B. `TMIN`, `TMAX`, `PRCP`) an, um welche Art von Wetterdaten es sich handelt.
Für die Anforderungen des Kunden sind die Minimal- und Maximaltemperaturen (`TMIN`, `TMAX`) relevant.

Beispielhaft sieht eine Zeile aus dem Datensatz wie folgt aus:
`GME00129502 200211 TMAX  142  E  103  E  147  E   81  E   72  E   81  E   43  E   48  E   81  E   56  E  107  E  100  E  100  E   80  E   82  E   89  E  114  E   62  E   61  E   72  E   89  E   56  E   70  E   89  E   85  E   67  E   66  E   72  E   78  E   68  E-9999

- GME00129502: Stations-ID
- 200211: Jahr und Monat: 2002, November
- TMAX: Gibt an, dass es sich um die maximalen Tageshöchsttemperaturen handelt
- 142: Die Zahlen repräsentieren die maximalen Tageshöchsttemperaturen für jeden Tag des Monats (in Zehntelgrad Celsius)
  - 142 entspricht 14.2 Grad Celsius
  - -9999 bedeutet, dass für diesen Tag keine Daten verfügbar sind (z. B. weil der November nur 30 Tage und nicht 31 Tage hat)
    - E: Ist das Source Flag und gibt an woher die Daten stammen. In diesem Beispiel stammen die Daten aus _European Climate Assessment & Dataset_
      (wenn die Daten aus einer anderen Datenquelle stammen, dann wird ein anderer Buchstabe verwendet - z. B. a = Australian data from the Australian Bureau of Meteorology)

--- 

## Quellen

- Link zu Datenquelle: https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/
- Link zu Wetterdaten einer Station:
  - https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/{station_id}.dly