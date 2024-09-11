from rest_framework import serializers
from .models import ElectricityData
from .models import WeatherData

# Serializer for the ElPriceResponse
class ElPriceResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricityData
        fields = ['NOK_per_kWh', 'EUR_per_kWh', 'EXR', 'time_start', 'time_end']
        

class ElPriceRequestSerializer(serializers.Serializer):
    region = serializers.CharField(required=False)  # Region is optional
    city = serializers.CharField(required=False)  # City is optional
    state = serializers.CharField(required=False)  # State is optional
    date = serializers.CharField()  # Date is required


# Serializer for the WeatherDataResponse
class WeatherDataResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = ['temperature', 'time_start', 'time_end']

# Serializer for the WeatherRequest
class WeatherRequestSerializer(serializers.Serializer):
    city = serializers.CharField(max_length=255)
    state = serializers.CharField(max_length=255)
    date = serializers.CharField()
