from rest_framework import serializers

from water_reminder.models import Water, WaterLog


class WaterLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterLog
        fields = ("intake", "intaked_time")


class WeatherSerializer(serializers.Serializer):
    temperature = serializers.IntegerField()
    condition = serializers.CharField(max_length=200)
    data = serializers.DateTimeField()
    icon_url = serializers.URLField()


class WaterIntakeSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.profiles.name")
    water_logs = WaterLogSerializer(many=True, read_only=True)

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
            "water_logs",
        )


class WaterSerializer(serializers.ModelSerializer):
    water_logs = WaterLogSerializer(many=True, read_only=True)

    class Meta:
        model = Water
        fields = (
            "id",
            "daily_intake",
            "intake_goal",
            "intake_achieved",
            "intake_status_percentage",
            "current_water_intake",
            "water_logs",
        )
        read_only_fields = (
            "id",
            "daily_intake",
            "intake_goal",
            "intake_achieved",
            "intake_status_percentage",
        )
