from django.contrib.auth import get_user_model
from django.utils import timezone
from celery import shared_task

from water_reminder_app.models import Water, WaterLog


@shared_task
def reset_daily_water_intake():
    users = get_user_model().objects.all()
    for user in users:
        try:
            water = Water.objects.get(user=user)
            WaterLog.objects.filter(water=water).delete()
            water.days += 1
            water.daily_intake = 0
            water.current_water_intake = 0
            water.intake_status_percentage = 0
            water.intake_achieved = False
            water.last_updated = timezone.now()
            water.save()
        except Water.DoesNotExist:
            pass
