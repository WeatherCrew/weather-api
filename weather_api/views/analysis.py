from rest_framework.views import APIView
from rest_framework.response import Response
from weather_api.utils.weather_data_downloader import download_dly_file
from weather_api.utils.weather_data_parser import parse_dly_file
from weather_api.utils.weather_data_analysis import calculate_annual_means, calculate_seasonal_means



class StationAnalysisView(APIView):
    # Kommentar fehlt noch

    def get(self, request):
        station_id = str(request.query_params.get("station_id"))
        start_year = int(request.query_params.get("start_year"))
        end_year = int(request.query_params.get("end_year"))

        if not station_id or not start_year or not end_year:
            return Response({"error": "Missing parameter(s)"}, status=400)

        try:
            dly_content = download_dly_file(station_id)

            data = parse_dly_file(dly_content)

            annual_means = calculate_annual_means(data, start_year, end_year)

            seasonal_means = calculate_seasonal_means(data, start_year, end_year)

            response_data = {
                "annual_means": annual_means.to_dict(orient="records"),
                "seasonal_means": seasonal_means.to_dict(orient="records")
            }
            return Response(response_data)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
