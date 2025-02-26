from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from weather_api.utils.stations_loader import stations_cache
from weather_api.utils.station_filters import filter_stations


class StationSearchView(APIView):
    """API view to search for weather stations near a given location.

    Handles GET requests to filter stations by geographic coordinates, radius, data availability and time period.
    Returns a list of matching stations from the cached station data.
    """
    @extend_schema(
        summary="Search for weather stations near a given location",
        description="Returns a list of weather stations within a specified radius and data availability period based on "
                    "geographic coordinates.",
        parameters=[
            OpenApiParameter(name="latitude", description="Latitude (-90 to 90)", required=True, type=float),
            OpenApiParameter(name="longitude", description="Longitude (-180 to 180)", required=True, type=float),
            OpenApiParameter(name="radius", description="Search radius in km", required=True, type=float),
            OpenApiParameter(name="max_results", description="Maximum number of results", required=True, type=int),
            OpenApiParameter(name="start_year", description="Start year of data availability", required=True, type=int),
            OpenApiParameter(name="end_year", description="End year of data availability", required=True, type=int),
        ],
        responses={
            200: OpenApiResponse(description="A list of weather stations matching the search criteria."),
            400: OpenApiResponse(description="Invalid query parameters provided."),
            500: OpenApiResponse(description="Internal server error due to missing station data."),
        },
    )

    def get(self, request):
        """Handles GET requests to search for weather stations.

        Extracts query parameters from the request, filter stations using the cached data, and returns the results as
        a JSON response.

        Args:
            request (rest_framework.request.Request): The incoming HTTP request containing query parameters:
                - latitude (float): Latitude (-90 to 90).
                - longitude (float): Longitude (-180 to 180).
                - radius (float): Search radius in kilometers.
                - max_results (int): Maximum number of results.
                - start_year (int): Start year of data availability.
                - end_year (int): End year of data availability.

        Returns:
            rest_framework.response.Response:JSON response with a list of matching stations.

        Raises:
            ValueError: If query parameters cannot be converted to the required types.
            TypeError: If required query parameters are missing or invalid.
        """
        try:
            latitude = float(request.query_params.get("latitude"))
            longitude = float(request.query_params.get("longitude"))
            radius = float(request.query_params.get("radius"))
            max_results = int(request.query_params.get("max_results"))
            start_year = int(request.query_params.get("start_year"))
            end_year = int(request.query_params.get("end_year"))

            stations = stations_cache["stations"]

            if not stations:
                return Response({"error": "Stations data not loaded"}, status=500)

            results = filter_stations(stations, latitude, longitude, radius, max_results, start_year, end_year)

            return Response(results)

        except (TypeError, ValueError):
            return Response({"error": "Invalid parameters"}, status=400)
