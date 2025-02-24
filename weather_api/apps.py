from django.apps import AppConfig
from weather_api.utils.stations_loader import initialize_station_data, stations_cache


class WeatherApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weather_api'

    def ready(self):
        """Load weather station data on application startup.

        Calls `initialize_station_data()`to load and cache station data when the Django application starts.

        Returns:
            None
        """
        stations_cache.update(initialize_station_data())
