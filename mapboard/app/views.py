from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ElPriceRequestSerializer, ElPriceResponseSerializer
from .utils import ElectricityPriceTool, WeatherDataTool
from .serializers import WeatherRequestSerializer, WeatherDataResponseSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class ElectricityPriceView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("Request data:", request.data)  # Log request data for debugging
        serializer = ElPriceRequestSerializer(data=request.data)
        if serializer.is_valid():
            data_tool = ElectricityPriceTool()
            prices = data_tool.get_electricity_prices(serializer.validated_data)

            if 'error' in prices:
                print("Error fetching prices:", prices)  # Log error for debugging
                return Response(prices, status=400)

            response_serializer = ElPriceResponseSerializer(prices, many=True)
            print("Prices response:", response_serializer.data)  # Log response for debugging
            return Response(response_serializer.data)

        print("Invalid request data:", serializer.errors)  # Log validation errors
        return Response(serializer.errors, status=400)


class WeatherDataView(APIView):

    def post(self, request):
        serializer = WeatherRequestSerializer(data=request.data)
        if serializer.is_valid():
            data_tool = WeatherDataTool()
            observations = data_tool.get_weather_data(serializer.validated_data)

            if 'error' in observations:
                return Response(observations, status=400)

            response_serializer = WeatherDataResponseSerializer(observations, many=True)
            return Response(response_serializer.data)

        return Response(serializer.errors, status=400)
