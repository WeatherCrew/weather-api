from rest_framework.views import APIView
from rest_framework.response import Response
from weather_api.utils.stations_file_loader import stations_cache, filter_stations


class StationSearchView(APIView):
    # Kommentar fehlt noch

    def get(self, request):
        latitude = float(request.query_params.get("latitude"))
        longitude = float(request.query_params.get("longitude"))
        radius = float(request.query_params.get("radius"))
        max_results = int(request.query_params.get("max_results"))

        stations = stations_cache["stations"]
        inventory = stations_cache["inventory"]

        if not stations or not inventory:
            return Response({"error": "Stations data not loaded"}, status=500)

        results = filter_stations(stations, latitude, longitude, radius, max_results, inventory)

        return Response(results)