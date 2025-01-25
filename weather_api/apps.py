from django.apps import AppConfig
from weather_api.utils.stations_file_loader import initialize_station_data


class WeatherApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weather_api'

    def ready(self):
        initialize_station_data()
