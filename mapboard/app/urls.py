from django.urls import path
from .views import WeatherDataView, ElectricityPriceView

urlpatterns = [
    path('api/weather-data/', WeatherDataView.as_view(), name='weather-data'),
    path('api/electricity-prices/', ElectricityPriceView.as_view(), name='electricity-prices'),
]
