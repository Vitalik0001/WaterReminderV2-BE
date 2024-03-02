from rest_framework import serializers

from water_reminder.models import Water


class WeatherSerializer(serializers.Serializer):
    temperature = serializers.IntegerField()
    condition = serializers.CharField(max_length=200)
    data = serializers.DateTimeField()
    icon_url = serializers.URLField()


class WaterIntakeSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.profiles.name")

    class Meta:
        model = Water
        fields = (
            "id",
            "user_name",
            "total_intake",
            "daily_intake",
            "average_intake",
            "intake_goal",
            "intake_achieved",
            "days",
        )
