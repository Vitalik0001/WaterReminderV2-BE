from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import UserProfile
from user.serializers import (
    UserCreateSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
)
from water_reminder.models import Water


class CalculateWaterIntake:

    def __init__(self, profile_instance):
        self.profile_instance = profile_instance

    def calculate_water_intake_goal(self):
        """Calculate water intake goal for user appropriate their parameters"""

        gender_multiplier = {
            "M": 0.04,
            "F": 0.03
        }

        activity_multiplier = {
            "M": 1.0,
            "L": 1.2,
            "A": 1.35,
            "H": 1.5,
            "V": 1.7,
        }

        water_intake = (
                self.profile_instance.weight
                * gender_multiplier[self.profile_instance.gender]
                * activity_multiplier[self.profile_instance.activity]
        )

        rounded_water_intake = round(water_intake * 1000)

        return rounded_water_intake


class UserCreateView(CreateAPIView):
    serializer_class = UserCreateSerializer


class UserProfileCreateView(APIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user_profile = serializer.save(user=request.user)
            calculate = CalculateWaterIntake(user_profile)
            intake_goal = calculate.calculate_water_intake_goal()
            Water.objects.create(user=user_profile.user, intake_goal=intake_goal)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileUpdateView(APIView):
    serializer_class = UserProfileUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = self.serializer_class(instance=user_profile)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        """Lists water intake if user update his weight or activity"""
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = self.serializer_class(user_profile, data=request.data, partial=True)

        activity_before = user_profile.activity
        weight_before = user_profile.weight

        if serializer.is_valid():
            serializer.save()

            weight_after = serializer.data["weight"]
            activity_after = serializer.data["activity"]

            if weight_before != weight_after or activity_before != activity_after:
                calculate = CalculateWaterIntake(user_profile)
                intake_goal = calculate.calculate_water_intake_goal()
                water_instance = Water.objects.get(user=request.user)
                water_instance.intake_goal = intake_goal
                water_instance.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
