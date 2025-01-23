# Beschreibung der vorliegenden Daten

In der vorliegenden Datenquelle des Daily Global Historical Climatology Network (GHCN) sind verschiedene Daten verfügbar. 
Um die Anforderungen des Kunden umzusetzen, werden einerseits Daten zu Wetterstationen (z. B. Koordinaten, Name etc.) 
und andererseits Wetterdaten (insbesondere Temperaturen) benötigt. Im Folgenden werden daher die für die Umsetzung des Projekts notwendigen Daten beschrieben.

---

## Stationsdaten

Der Benutzer der Wetter-App gibt folgende Daten ein: Geografische Länge, Breite, einen Suchradius und die maximale Anzahl der Stationen, die angezeigt werden sollen.
Basierend darauf solle die Wetterstationen gefunden werden, die sich innerhalb des angegebenen Radius um den Standort des Benutzers befinden.
Um diese Anforderung umzusetzen, werden die folgenden Dateien benötigt: 
- `ghcnd-stations.csv` (https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.csv)
- `ghcnd-inventory.txt` (https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-inventory.txt)

### ghcnd-stations.csv

Die Datei wird benötigt, um die Wetterstationen zu finden, die sich innerhalb des Radius um den angegebenen Standort befinden.
Die Datei enthält folgende Informationen zu den Wetterstationen:

## Format of "ghcnd-stations.txt"

| **Variable**   | **Columns** | **Type**     |
|-----------------|-------------|--------------|
| ID             | 1-11        | Character    |
| LATITUDE       | 13-20       | Real         |
| LONGITUDE      | 22-30       | Real         |
| ELEVATION      | 32-37       | Real         |
| STATE          | 39-40       | Character    |
| NAME           | 42-71       | Character    |
| GSN FLAG       | 73-75       | Character    |
| HCN/CRN FLAG   | 77-79       | Character    |
| WMO ID         | 81-85       | Character    |

---

### Variable Definitions

- **ID**  
  The station identification code. The first two characters denote the FIPS country code, the third character is a network code that identifies the station numbering system used, and the remaining eight characters contain the actual station ID.  
  - See `ghcnd-countries.txt` for a complete list of country codes.  
  - See `ghcnd-states.txt` for a list of state/province/territory codes.

  **Network Code Values**:  
  - `0`: Unspecified (station identified by up to eight alphanumeric characters).  
  - `1`: Community Collaborative Rain, Hail, and Snow (CoCoRaHS) based identification number.  
  - `C`: U.S. Cooperative Network identification number (last six characters of the GHCN-Daily ID).  
  - `E`: Identification number used in the ECA&D non-blended dataset.  
  - `M`: World Meteorological Organization ID (last five characters of the GHCN-Daily ID).  
  - `N`: Identification number used in data supplied by a National Meteorological or Hydrological Center.  
  - `P`: "Pre-Coop" (an internal identifier assigned by NCEI for station records collected prior to the establishment of the U.S. Weather Bureau).  
  - `R`: U.S. Interagency Remote Automatic Weather Station (RAWS) identifier.  
  - `S`: U.S. Natural Resources Conservation Service SNOTEL station identifier.  
  - `W`: WBAN identification number (last five characters of the GHCN-Daily ID).

- **LATITUDE**  
  The latitude of the station (in decimal degrees).

- **LONGITUDE**  
  The longitude of the station (in decimal degrees).

- **ELEVATION**  
  The elevation of the station (in meters, missing = -999.9).

- **STATE**  
  The U.S. postal code for the state (for U.S. stations only).

- **NAME**  
  The name of the station.

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


Die liefert jedoch keine Iformationen darüber, in welchem Zeitraum bzw. in welchen Jahren Wetterdaten verfügbar sind.
Dafür kommt die Datei `ghcnd-inventory.txt` zum Einsatz.

### ghcnd-inventory.txt

Die Datei enthält ebenfalls Informationen zu Wetterstationen, wie z. B. die ID, Länge und Breite. Zusätzliche enthält sie jedoch
auch Informationen über den Zeitraum, für den Wetterdaten verfügbar sind.

Die Datei enthält folgende Informationen:

| **Variable** | **Type**     |
|--------------|--------------|
| ID           | Character    |
| LATITUDE     | Real         |
| LONGITUDE    | Real         |
| ELEMENT      | Character    |
| FIRSTYEAR    | Integer      |
| LASTYEAR     | Integer      |


- **ID**:  
  The station identification code. Please see `ghcnd-stations.txt` for a complete list of stations and their metadata.

- **LATITUDE**:  
  The latitude of the station (in decimal degrees).

- **LONGITUDE**:  
  The longitude of the station (in decimal degrees).

- **ELEMENT**:  
  The element type. See section III for a definition of elements.

- **FIRSTYEAR**:  
  The first year of unflagged data for the given element.

- **LASTYEAR**:  
  The last year of unflagged data for the given element.

---

## Wetterdaten zu einer Station:

--- 

## Source

- Link zur Datenquelle:
- Stationsdaten: 
- Wetterdaten zu einer Wetterstation: