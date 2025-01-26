from math import radians, sin, cos, sqrt, atan2

# Evtl. Python-Modul nutzen, um die Distanz zwischen zwei Koordinaten zu berechnen??


def haversine(lat1, lon1, lat2, lon2):
    # Kommentar fehlt noch
    R = 6371  # radius of earth in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = (2 * atan2(sqrt(a), sqrt(1 - a)))  # atan2(sqrt(a), sqrt(1-a)) is equivalent

    return R * c
