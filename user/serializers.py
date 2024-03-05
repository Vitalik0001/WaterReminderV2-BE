from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.models import UserProfile


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password", "is_staff")
        read_only_fields = ("id", "is_staff")

        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def create(self, validated_data):
        """Create user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "id",
            "profile_image",
            "gender",
            "name",
            "age",
            "weight",
            "height",
            "activity",
        )
        read_only_fields = ("id", "profile_image")


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "id",
            "profile_image",
            "gender",
            "name",
            "age",
            "weight",
            "height",
            "activity",
        )
        read_only_fields = (
            "id",
            "profile_image",
            "gender",
            "name",
        )
