from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from weather_api.utils.stations_file_loader import stations_cache, filter_stations


class StationSearchView(APIView):
    # Kommentar fehlt noch
    @extend_schema(
        summary="Searches for weather stations in the near of a given position",
        description="Returns a list of weather stations based on the specified geo coordinates.",
        parameters=[
            OpenApiParameter(name="latitude", description="Latitude", required=True, type=float),
            OpenApiParameter(name="longitude", description="Longitude", required=True, type=float),
            OpenApiParameter(name="radius", description="Search radius in km", required=True, type=float),
            OpenApiParameter(name="max_results", description="Maximum number of results", required=True, type=int),
        ],
        responses={200: "List of weather stations"},
    )

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