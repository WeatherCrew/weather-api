from django.urls import path
from weather_api.views.search import StationSearchView

urlpatterns = [
    path('stations/search/', StationSearchView.as_view(), name='station_search')
]
