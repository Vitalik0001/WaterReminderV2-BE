import random
import requests

from rest_framework import status
from urllib.parse import urljoin
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView

from water_reminder.settings import API_KEY
from water_reminder_app.models import Water, GidrationTip
from water_reminder_app.serializers import (
    WaterIntakeSerializer,
    WeatherSerializer,
    WaterSerializer,
    GidrationTipSerializer,
)


def get_three_gidration_tips():
    """Return a queryset containing three randomly selected gidration tips"""
    pks = GidrationTip.objects.values_list("pk", flat=True)
    random_pk_list = [random.choice(pks) for _ in range(3)]
    gidration_tips = GidrationTip.objects.filter(id__in=random_pk_list)

    return gidration_tips


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
        """Process raw weather data into a more structured format."""
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
        water = get_object_or_404(
            Water.objects.select_related("user"), user=request.user
        )
        water_serializer = WaterIntakeSerializer(instance=water)

        gidration_tips = get_three_gidration_tips()
        gidration_tips_serializer = GidrationTipSerializer(gidration_tips, many=True)

        weather_data = WeatherDataFetcher.get_weather_data()
        processed_weather_data = WeatherDataFetcher.process_weather_data(weather_data)

        if processed_weather_data:
            weather_serializer = WeatherSerializer(instance=processed_weather_data)

        return Response(
            {
                "water_intake": water_serializer.data,
                "weather": weather_serializer.data,
                "gidration_tips": gidration_tips_serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class WaterView(RetrieveUpdateAPIView):
    serializer_class = WaterSerializer

    def get_object(self):
        water_instance = Water.objects.prefetch_related("water_logs").get(
            user=self.request.user
        )

        return water_instance
