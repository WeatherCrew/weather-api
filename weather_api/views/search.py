from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from weather_api.utils.stations_file_loader_simple import stations_cache, filter_stations


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
            OpenApiParameter(name="start_year", description="Start year of data availability", required=True, type=int),
            OpenApiParameter(name="end_year", description="End year of data availability", required=True, type=int),
        ],
        responses={
            200: {
                "description": "List of weather stations",
                "examples": {
                    "application/json": [
                        {
                            "station_id": "GME00129502",
                            "name": "BERLIN-DAHLEM",
                            "latitude": 48.0092,
                            "longitude": 8.8189,
                            "distance": 1.23,
                            "data_availability": {"first_year": 1991, "last_year": 2003}
                        }
                    ]
                }
            }
        }
    )

    def get(self, request):
        try:
            latitude = float(request.query_params.get("latitude"))
            longitude = float(request.query_params.get("longitude"))
            radius = float(request.query_params.get("radius"))
            max_results = int(request.query_params.get("max_results"))
            start_year = int(request.query_params.get("start_year"))
            end_year = int(request.query_params.get("end_year"))

            """
            stations = stations_cache["stations"]
            inventory = stations_cache["inventory"]
            
            
            
            if not stations or not inventory:
                return Response({"error": "Stations data not loaded"}, status=500)
            """

            stations = stations_cache["stations"]

            if not stations:
                return Response({"error": "Stations data not loaded"}, status=500)

            results = filter_stations(stations, latitude, longitude, radius, max_results, start_year, end_year)

            return Response(results)

        except (TypeError, ValueError):
            return Response({"error": "Invalid parameters"}, status=400)
