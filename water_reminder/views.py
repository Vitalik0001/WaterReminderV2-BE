import requests
from urllib.parse import urljoin
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView

from app.settings import API_KEY
from water_reminder.models import Water
from water_reminder.serializers import (
    WaterIntakeSerializer,
    WeatherSerializer,
    WaterSerializer,
)


class WeatherDataFetcher:
    @staticmethod
    def get_current_location():
        """Return current city with using 'ipinfo.io' by IP"""
        url = "http://ipinfo.io/json"
        response = requests.get(url).json()

        return response["city"]

    @staticmethod
    def get_weather_data():
        """Extract weather data from 'api.weatherapi.com' API"""
        city = WeatherDataFetcher.get_current_location()
        response = requests.get(
            f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"
        )
        response.raise_for_status()

        return response.json()

    @staticmethod
    def process_weather_data(weather_data):
        """ Process raw weather data into a more structured format."""
        if weather_data:
            temperature = round(weather_data["current"]["temp_c"])
            condition = weather_data["current"]["condition"]["text"]
            data = weather_data["location"]["localtime"].split()[0]
            icon_relative_url = weather_data["current"]["condition"]["icon"]
            icon_url = urljoin("https:", icon_relative_url)

            processed_data = {
                "temperature": temperature,
                "condition": condition,
                "data": data,
                "icon_url": icon_url,
            }
            return processed_data

        return None


class DashboardView(APIView):
    def get(self, request):
        water = Water.objects.get(user=request.user)
        water_serializer = WaterIntakeSerializer(instance=water)

        weather_data = WeatherDataFetcher.get_weather_data()
        processed_weather_data = WeatherDataFetcher.process_weather_data(weather_data)

        if processed_weather_data:
            weather_serializer = WeatherSerializer(instance=processed_weather_data)

        return Response(
            {"water_intake": water_serializer.data, "weather": weather_serializer.data},
            status=status.HTTP_200_OK,
        )


class WaterView(RetrieveUpdateAPIView):
    serializer_class = WaterSerializer

    def get_object(self):
        return Water.objects.get(user=self.request.user)
