import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from weather_api.utils.weather_data_downloader import download_dly_file
from weather_api.utils.weather_data_parser import parse_dly_file
from weather_api.utils.weather_data_analysis import calculate_annual_means, calculate_seasonal_means
from weather_api.utils.stations_file_loader_simple import stations_cache
from weather_api.utils.response_builder import build_weather_data_response

class StationAnalysisView(APIView):
    # Noch Prüfung einbauen, dass end_year > start_year -> dann Fehlermeldung

    @extend_schema(
        summary="Analyzes weather data for a specific station",
        description=(
            "Noch hinzufügen"
        ),
        parameters=[
            OpenApiParameter(
                name="station_id",
                type=str,
                location=OpenApiParameter.QUERY,
                required=True,
                description="StationID of the weather station",
            ),
            OpenApiParameter(
                name="start_year",
                type=int,
                location=OpenApiParameter.QUERY,
                required=True,
                description="First year for that weather data should be analyzed.",
            ),
            OpenApiParameter(
                name="end_year",
                type=int,
                location=OpenApiParameter.QUERY,
                required=True,
                description="Last year for that weather data should be analyzed.",
            ),
        ],
        responses={
            200: {
                "description": "Successfully retrieved and analysed weather data.",
                "content": {
                    "application/json": {
                        "example": {
                            "annual_means": [
                                {"YEAR": 2010, "TMIN": 1.2, "TMAX": 10.5},
                                {"YEAR": 2011, "TMIN": 2.0, "TMAX": 11.0},
                            ],
                            "seasonal_means": [
                                {"YEAR": 2010, "SEASON": "winter", "TMIN": -1.2, "TMAX": 4.5},
                                {"YEAR": 2010, "SEASON": "spring", "TMIN": 2.0, "TMAX": 15.0},
                            ],
                        }
                    }
                },
            },
            400: {"description": "Missing or invalid parameter(s)"},
            504: {"description": "Timeout while downloading data"},
            500: {"description": "Internal Server Error"},
        },
    )
    def get(self, request):
        station_id = request.query_params.get("station_id")
        start_year = request.query_params.get("start_year")
        end_year = request.query_params.get("end_year")

        if not station_id or not start_year or not end_year:
            return Response({"error": "Missing parameter(s)"}, status=400)

        # prüfen, ob start_year < end_year??

        try:
            start_year = int(start_year)
            end_year = int(end_year)
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

            # replace nan with None, because JSON does not support NaN (is there another way to directly fix it? Use None instead of NaN?)
            annual = annual.replace({pd.NA: None, float('nan'): None})
            seasonal = seasonal.replace({pd.NA: None, float('nan'): None})

            annual_list = annual.to_dict(orient="records")
            seasonal_list = seasonal.to_dict(orient="records")

            # runden auf eine Nachkommastelle?
            response_data = build_weather_data_response(annual_list, seasonal_list)

            return Response(response_data)


        except TimeoutError as te:
            return Response({"error": str(te)}, status=504)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
