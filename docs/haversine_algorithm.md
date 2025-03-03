# Haversine-Algorithmus zur Distanzberechnung

---

## Zweck

Der Haversine-Algorithmus berechnet die Distanz zwischen zwei Punkten auf einer Kugel (in diesem Fall der Erde) anhand 
ihrer geografischen Koordinaten (Breitengrad und Längengrad).

---

## Algorithmusbeschreibung

### Mathematische Formel

Die Haversine-Formel berechnet die Distanz d zwischen zwei Punkten auf einer Kugel mit Radius R:

1. Eingabedaten:
   - lat₁, lon₁: Koordinaten des ersten Punktes
   - lat₂, lon₂: Koordinaten des zweiten Punktes

2. Umrechnung in Radiant:
   - Alle Koordinaten müssen von Grad in Radiant umgerechnet werden
   - Umrechnung: rad = grad · π/180

3. Berechnung mit der Haversine-Formel:
   - Δlat = lat₂ - lat₁ (Differenz der Breitengrade)
   - Δlon = lon₂ - lon₁ (Differenz der Längengrade)
   - a = sin²(Δlat/2) + cos(lat₁) · cos(lat₂) · sin²(Δlon/2)
   - c = 2 · atan2(√a, √(1-a))
   - d = R · c (R = Erdradius - 6371 km)

4. Das Ergebnis d ist die Distanz zwischen den beiden Punkten.

### Python-Modul `haversine`

Es gibt auch ein Python-Modul namens `haversine`, das die Berechnung der Distanz zwischen zwei Koordinaten ermöglicht.

---

## Quellen

- https://en.wikipedia.org/wiki/Haversine_formula
- https://medium.com/@herihermawan/comparing-the-haversine-and-vincenty-algorithms-for-calculating-great-circle-distance-5a2165857666