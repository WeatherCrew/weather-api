from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from weather_api.utils.weather_data_downloader import download_dly_file
from weather_api.utils.weather_data_parser import parse_dly_file
from weather_api.utils.weather_data_analysis import preprocess_weather_data, calculate_annual_means, calculate_seasonal_means
from weather_api.utils.stations_loader import stations_cache
from weather_api.utils.weather_data_response_builder import build_weather_data_response

class StationAnalysisView(APIView):
    """API view to analyze weather data for a specific station.

    Handles requests to download, parse and analyze weather data, providing annual and seasonal temperature means for
    a given station and time period.
    """
    @extend_schema(
        summary="Analyzes weather data for a specific station",
        description="Downloads and analyzes weather data for a given station, returning annual and seasonal "
                     "temperature means for the specified time period.",
        parameters=[
            OpenApiParameter(name="station_id", description="StationID of the weather station", required=True, type=str),
            OpenApiParameter(name="start_year", description="First year of the analysis period", required=True, type=int),
            OpenApiParameter(name="end_year", description="Last year of the analysis period", required=True, type=int),
        ],
        responses={
            200: OpenApiResponse(description="Successfully retrieved and analyzed weather data."),
            400: OpenApiResponse(description="Invalid or missing query parameters provided."),
            404: OpenApiResponse(description="Station not found in cached data."),
            504: OpenApiResponse(description="Timeout occurred while downloading weather data."),
            500: OpenApiResponse(description="Internal server error during processing."),
        },
    )
    def get(self, request):
        """Handles GET requests to analyze weather data for a given station.

        Downloads weather data for a given station, parse it, calculates annual and seasonal means based on the
        specified time period, and returns the results as a JSON response.

        Args:
            request (rest_framework.request.Request): The incoming HTTP request containing query parameters:
                - station_id (str): ID of the weather station to analyze.
                - start_year (int): First year of the analysis period.
                - end_year (int): Last year of the analysis period.

        Returns:
            rest_framework.response.Response: A JSON response containing annual and seasonal means for the station, or
            an error response with an appropriate status code.
        """
        try:
            station_id = request.query_params.get("station_id")
            start_year = request.query_params.get("start_year")
            end_year = request.query_params.get("end_year")

            if not station_id or not start_year or not end_year:
                return Response({"error": "Missing parameter(s)"}, status=400)

            start_year = int(start_year)
            end_year = int(end_year)

            if start_year > end_year:
                return Response({"start_year must <= end_year"}, status=400)

            file_content = download_dly_file(station_id)
            parsed_data = parse_dly_file(file_content, start_year, end_year)

            stations_data = stations_cache["stations"].get(station_id)
            if stations_data is None:
                return Response({"error": "Station not found"}, status=404)
            hemisphere = stations_data.get("hemisphere")

            preprocessed_data = preprocess_weather_data(parsed_data)
            annual = calculate_annual_means(preprocessed_data, start_year, end_year)
            seasonal = calculate_seasonal_means(preprocessed_data, start_year, end_year, hemisphere)

            annual_list = annual.to_dict(orient="records")
            seasonal_list = seasonal.to_dict(orient="records")

            response_data = build_weather_data_response(annual_list, seasonal_list)

            return Response(response_data)

        except TimeoutError as te:
            return Response({"error": str(te)}, status=504)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
