from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password")
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 8}
        }

    def create(self, validated_data):
        """Create user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)
