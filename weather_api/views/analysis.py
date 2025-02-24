import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from weather_api.utils.weather_data_downloader import download_dly_file
from weather_api.utils.weather_data_parser import parse_dly_file
from weather_api.utils.weather_data_analysis import calculate_annual_means, calculate_seasonal_means
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
            200: {
                "description": "Successfully retrieved and analyzed weather data.",
                "content": {
                    "application/json": {
                        "example": {
                            "years": [
                                {
                                    "year": 2000,
                                    "annual_means": {
                                        "tmin": 3.949453551912568,
                                        "tmax": 13.532240437158471
                                    },
                                    "seasonal_means": {
                                        "winter": {"tmin": -3.1725274725274724, "tmax": 3.6868131868131866},
                                        "spring": {"tmin": 3.319565217391304, "tmax": 14.133695652173913},
                                        "summer": {"tmin": 9.764130434782608, "tmax": 22.003260869565217},
                                        "autumn": {"tmin": 4.99010989010989, "tmax": 13.45054945054945}
                                    }
                                },
                                {
                                    "year": 2001,
                                    "annual_means": {
                                        "tmin": 3.446849315068493,
                                        "tmax": 12.767397260273974
                                    },
                                    "seasonal_means": {
                                        "winter": {"tmin": -2.387777777777778, "tmax": 4.866666666666666},
                                        "spring": {"tmin": 3.847826086956522, "tmax": 12.742391304347825},
                                        "summer": {"tmin": 9.883695652173913, "tmax": 22.181521739130435},
                                        "autumn": {"tmin": 3.756043956043956, "tmax": 12.462637362637361}
                                    }
                                }
                            ]
                        }
                    }
                },
            },
            400: {
                "description": "Invalid or missing query parameters provided.",
                "examples": {
                    "application/json": {"error": "Missing parameter(s)"}
                }
            },
            404: {
                "description": "Station not found in cached data.",
                "examples": {
                    "application/json": {"error": "Station not found"}
                }
            },
            504: {
                "description": "Timeout occurred while downloading weather data.",
                "examples": {
                    "application/json": {"error": "Timeout while downloading data"}
                }
            },
            500: {
                "description": "Internal server error during processing.",
                "examples": {
                    "application/json": {"error": "Internal Server Error"}
                }
            },
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
            rest_framework.response.Response: A JSON response containing annual and seasonal means for the station.

        Raises:
            ValueError: If start_year or end_year cannot be converted to integers or start_year > end_year.
            TypeError: If required query parameters are missing or invalid.
        """
        station_id = request.query_params.get("station_id")
        start_year = request.query_params.get("start_year")
        end_year = request.query_params.get("end_year")

        if not station_id or not start_year or not end_year:
            return Response({"error": "Missing parameter(s)"}, status=400)

        try:
            start_year = int(start_year)
            end_year = int(end_year)

            if start_year > end_year:
                raise ValueError("start_year must be less than or equal to end_year")
        except ValueError:
            return Response({"error": "start_year and end_year must be integers"}, status=400)

        try:
            file_content = download_dly_file(station_id)
            parsed_data = parse_dly_file(file_content)

            stations_data = stations_cache["stations"].get(station_id)
            if stations_data is None:
                return Response({"error": "Station not found"}, status=404)
            hemisphere = stations_data.get("hemisphere")

            annual = calculate_annual_means(parsed_data, start_year, end_year)
            seasonal = calculate_seasonal_means(parsed_data, start_year, end_year, hemisphere)

            # Replace NaN with None for JSON compatibility
            annual = annual.replace({pd.NA: None, float('nan'): None})
            seasonal = seasonal.replace({pd.NA: None, float('nan'): None})

            # Convert DataFrames to list of dictionaries
            annual_list = annual.to_dict(orient="records")
            seasonal_list = seasonal.to_dict(orient="records")

            # Build structured JSON response
            response_data = build_weather_data_response(annual_list, seasonal_list)

            return Response(response_data)

        except TimeoutError as te:
            return Response({"error": str(te)}, status=504)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
