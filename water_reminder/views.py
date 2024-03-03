import requests
from urllib.parse import urljoin
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView

from app.settings import API_KEY, CITY
from water_reminder.models import Water
from water_reminder.serializers import (
    WaterIntakeSerializer,
    WeatherSerializer,
    WaterSerializer,
)


class DashboardView(APIView):
    def get(self, request):
        water = Water.objects.get(user=request.user)
        water_serializer = WaterIntakeSerializer(instance=water)

        weather_data = self.get_weather_data()
        processed_weather_data = self.process_weather_data(weather_data)

        if processed_weather_data:
            weather_serializer = WeatherSerializer(instance=processed_weather_data)

        return Response(
            {"water_intake": water_serializer.data, "weather": weather_serializer.data},
            status=status.HTTP_200_OK,
        )

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

    @staticmethod
    def get_weather_data():
        """Extract weather data from 'api.weatherapi.com' API"""
        response = requests.get(
            f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={CITY}&aqi=no"
        )
        response.raise_for_status()
        return response.json()


class WaterView(RetrieveUpdateAPIView):
    serializer_class = WaterSerializer

    def get_object(self):
        return Water.objects.get(user=self.request.user)
