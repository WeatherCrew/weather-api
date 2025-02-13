from django.urls import path
from weather_api.views.search import StationSearchView
from weather_api.views.analysis import  StationAnalysisView

urlpatterns = [
    path('stations/search/', StationSearchView.as_view(), name='station_search'),
    path('stations/analysis/', StationAnalysisView.as_view(), name='station_analysis')
]
