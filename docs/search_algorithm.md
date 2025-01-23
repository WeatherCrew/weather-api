# Algorithmus zur Suche von Wetterstationen

---

## Zweck

Der Algorithmus zur Suche von Wetterstationen ermittelt alle Wetterstationen, die sich innerhalb eines bestimmten Radius um einen
angegebenen Standort (angegeben durch Breiten- und Längengrad) befinden.

---

## Algorithmusbeschreibung

1. Eingabedaten:
    - Koordinaten: `latitude` und `longitude` des Standorts
    - Radius: Maximale Entfernung vom angegebenen Standort, innerhalb dessen nach Wetterstationen gesucht werden soll
    - Wetterstationen: Liste aller Wetterstationen mit ihren jeweiligen Koordinaten
2. Schritte des Algorithmus
    - Distanzberechnung: Für jede Wetterstation wird die Entfernung zum angegebenen Standort berechnet. Hierfür wird
         die Haversine-Formel verwendet.
    - Haversine-Formel:
      - a = sin²(Δ*lat/2) + cos(lat1) ⋅ cos(lat2) ⋅ sin²(Δlon/2)
      - c = 2 ⋅ atan2( √a, √(1−a) )
      - d = R ⋅ c (R ist der Erdradius(6371 km))
      - Es gibt auch ein Python Modul namens `haversine` für die Berechnung der Distanz zwischen zwei Koordinaten.
      - Filterung: Wetterstationen, die sich innerhalb des angegebenen Radius befinden, werden gespeichert.
      - Ausgabe: Rückgabe der Wetterstationen, die sich innerhalb des angegebene Radius befinden.

---

## Quellen

- https://medium.com/@herihermawan/comparing-the-haversine-and-vincenty-algorithms-for-calculating-great-circle-distance-5a2165857666
- https://pypi.org/project/haversine/

