from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from weather_api.utils.weather_data_downloader import download_dly_file
from weather_api.utils.weather_data_parser import parse_dly_file
from weather_api.utils.weather_data_analysis import calculate_annual_means, calculate_seasonal_means


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
                "description": "Erfolgreiche Antwort mit den berechneten Jahres- und Saisonwerten.",
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
        # Parameter aus den Query-Parametern abrufen
        station_id = request.query_params.get("station_id")
        start_year = request.query_params.get("start_year")
        end_year = request.query_params.get("end_year")

        if not station_id or not start_year or not end_year:
            return Response({"error": "Missing parameter(s)"}, status=400)

        try:
            start_year = int(start_year)
            end_year = int(end_year)
        except ValueError:
            return Response({"error": "start_year and end_year must be integers"}, status=400)

        try:
            # Download der Rohdaten
            file_content = download_dly_file(station_id)
            # Parsen der Daten
            parsed_data = parse_dly_file(file_content)
            # Berechnung der jährlichen Mittelwerte
            annual = calculate_annual_means(parsed_data, start_year, end_year)
            # Berechnung der saisonalen Mittelwerte
            seasonal = calculate_seasonal_means(parsed_data, start_year, end_year)

            # Konvertiere die Ergebnisse in ein Dictionary-Format für die JSON-Antwort
            annual_list = annual.to_dict(orient="records")
            seasonal_list = seasonal.to_dict(orient="records")


            # Diese Funktionalität noch in eine extra Funktion schreiben (zur Übersichtlichkeit)
            years_dict = {}

            for row in annual_list:
                year = row["YEAR"]
                years_dict[year] = {
                    "year": year,
                    "annual_means": {
                        "tmin": row["TMIN"],
                        "tmax": row["TMAX"]
                    },
                    "seasonal_means": {}
                }

            for row in seasonal_list:
                year = row["YEAR"]
                season = row["season"]
                if year in years_dict:
                    years_dict[year]["seasonal_means"][season] = {
                        "tmin": row["TMIN"],
                        "tmax": row["TMAX"]
                    }
            years = [years_dict[y] for y in sorted(years_dict)]

            response_data = {
                "years": years
            }

            return Response(response_data)

        except TimeoutError as te:
            return Response({"error": str(te)}, status=504)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
