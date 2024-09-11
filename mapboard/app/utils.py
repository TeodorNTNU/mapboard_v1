from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import requests_cache
from .models import ElectricityData, WeatherData
from django.db import transaction
from openmeteo_requests import Client
import pandas as pd
import retry
from functools import lru_cache
from retry_requests import retry
import requests_cache
import openmeteo_requests

# Utility function to parse date ranges
def parse_date(date: str):
    try:
        if '/' in date:
            start_date_str, end_date_str = date.split('/')
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        else:
            start_date = end_date = datetime.strptime(date, '%Y-%m-%d')
        
        if start_date > end_date:
            raise ValueError("Start date cannot be after end date.")
        
        return start_date, end_date
    except ValueError as e:
        raise ValueError(f"Invalid date format: {date}. Expected format is YYYY-MM-DD or YYYY-MM-DD/YYYY-MM-DD.")

# Geolocation base class
class BaseDataTool:
    geolocator = Nominatim(user_agent="data_tool_api")

    def get_coordinates(self, city_name: str, state: str):
        location = self.geolocator.geocode(f"{city_name}, {state}")
        return (location.latitude, location.longitude) if location else None


class ElectricityPriceTool(BaseDataTool):
    REGIONS = {
        "NO1": ("Oslo", (59.9139, 10.7522)),
        "NO2": ("Kristiansand", (58.1467, 7.9956)),
        "NO3": ("Trondheim", (63.4305, 10.3951)),
        "NO4": ("Tromsø", (69.6492, 18.9553)),
        "NO5": ("Bergen", (60.3928, 5.3221)),
    }

    session = requests_cache.CachedSession('electricity_cache', expire_after=86400)

    def find_nearest_region(self, lat, lon):
        """Finds the nearest predefined region based on latitude and longitude."""
        nearest_region = min(
            self.REGIONS.items(),
            key=lambda region: geodesic((lat, lon), region[1][1]).kilometers
        )[0]
        return nearest_region

    def fetch_electricity_prices(self, date, region):
        """Fetches electricity prices for a specific region and date."""
        year, month, day = date.split('-')
        url = f"https://www.hvakosterstrommen.no/api/v1/prices/{year}/{month}-{day}_{region}.json"
        response = self.session.get(url)

        if response.status_code == 200:
            return response.json()
        return {"error": f"Error fetching data: {response.status_code}"}

    @transaction.atomic
    def store_prices(self, request, region, prices):
        """Stores electricity prices in the database, using update_or_create to avoid duplication."""
        for price in prices:
            ElectricityData.objects.update_or_create(
                region=region,
                date=datetime.strptime(request['date'], '%Y-%m-%d').date(),
                time_start=price["time_start"],
                defaults={
                    'NOK_per_kWh': price["NOK_per_kWh"],
                    'EUR_per_kWh': price["EUR_per_kWh"],
                    'EXR': price["EXR"],
                    'time_end': price["time_end"],
                    'city': request.get('city', ''),
                    'state': request.get('state', ''),
                }
            )

    def get_electricity_prices(self, request):
        """Handles the entire process of getting electricity prices, including geolocation and fetching."""
        if 'region' in request:
            # Use the provided region directly
            region = request['region']
        else:
            # Translate city and state to coordinates and find the nearest region
            coordinates = self.get_coordinates(request['city'], request['state'])
            if not coordinates:
                return {"error": "City not found"}
            
            lat, lon = coordinates
            region = self.find_nearest_region(lat, lon)

        # Fetch electricity prices for the date range
        start_date, end_date = parse_date(request['date'])
        all_prices = []

        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            prices = self.fetch_electricity_prices(date_str, region)
            if isinstance(prices, list):
                self.store_prices({**request, 'date': date_str}, region, prices)
                all_prices.extend(prices)
            current_date += timedelta(days=1)

        return all_prices if all_prices else {"error": "No data found for the given date range."}




class WeatherDataTool(BaseDataTool):
    cache_session = requests_cache.CachedSession('.weather_cache', expire_after=-1)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = Client(session=retry_session)

    @transaction.atomic
    def store_weather_data(self, request, observations):
        """Stores weather data in the database, using update_or_create to avoid duplication."""
        for observation in observations:
            WeatherData.objects.update_or_create(
                city=request.get('city', ''),
                state=request.get('state', ''),
                date=datetime.strptime(observation['date'], '%Y-%m-%d').date(),
                time_start=observation['time_start'],
                defaults={
                    'temperature': observation['temperature'],
                    'time_end': observation['time_end'],
                }
            )

    def get_weather_data(self, request):
        """Fetches weather data for a region or city/state."""
        if 'region' in request:
            # Use the provided region to get coordinates
            region_data = self.REGIONS.get(request['region'])
            if not region_data:
                return {"error": "Invalid region"}
            latitude, longitude = region_data[1]
        else:
            # Otherwise, translate city and state to coordinates
            coordinates = self.get_coordinates(request['city'], request['state'])
            if not coordinates:
                return {"error": "Could not find coordinates for the specified city and state."}
            latitude, longitude = coordinates

        # Fetch weather data for the date range
        start_date, end_date = parse_date(request['date'])
        all_observations = []
        current_date = start_date

        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "start_date": date_str,
                "end_date": date_str,
                "hourly": "temperature_2m"
            }
            response = self.openmeteo.weather_api("https://archive-api.open-meteo.com/v1/archive", params=params)[0]

            hourly = response.Hourly()
            hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

            hourly_dates = pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            ).strftime('%Y-%m-%dT%H:%M:%S%z')

            observations = [
                {
                    "date": date_str,
                    "temperature": float(hourly_temperature_2m[i]),
                    "time_start": hourly_dates[i],
                    "time_end": hourly_dates[i + 1]
                }
                for i in range(len(hourly_dates) - 1)
            ]

            all_observations.extend(observations)
            current_date += timedelta(days=1)

        self.store_weather_data(request, all_observations)

        return all_observations

