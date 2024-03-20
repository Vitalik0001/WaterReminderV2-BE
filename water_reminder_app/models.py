import os
import uuid

from django.utils.text import slugify
from django.conf import settings
from django.db import models
from django.utils import timezone


def get_tip_image(instance, file_name):
    _, extension = os.path.splitext(file_name)
    file_path = f"{slugify(instance.name)}-{uuid.uuid4()}.{extension}"
    return os.path.join("uploads/tips/", file_path)


class Water(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="waters"
    )
    total_intake = models.IntegerField(default=0)
    daily_intake = models.IntegerField(default=0)
    average_intake = models.IntegerField(default=0.0)
    intake_goal = models.IntegerField(default=0)
    current_water_intake = models.IntegerField(default=0)
    intake_status_percentage = models.IntegerField(default=0)
    days = models.IntegerField(default=1)
    intake_achieved = models.BooleanField(default=False)
    last_updated = models.DateField(default=timezone.now)

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.pk:
            water_instance = Water.objects.get(pk=self.pk)

            old_daily_intake = water_instance.daily_intake
            day_before = water_instance.days

            if self.current_water_intake > 0:
                WaterLog.objects.create(
                    water=water_instance,
                    intake=self.current_water_intake
                )
                self.daily_intake += self.current_water_intake
                self.intake_status_percentage = (
                        self.daily_intake / self.intake_goal * 100
                )
                self.current_water_intake = 0

            if self.daily_intake >= self.intake_goal:
                self.intake_achieved = True

            if self.daily_intake > old_daily_intake:
                self.total_intake += self.daily_intake - old_daily_intake
                self.average_intake = self.total_intake / self.days

            if self.days > day_before:
                self.average_intake = self.total_intake / self.days

        self.last_updated = timezone.now()

        super().save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )


class WaterLog(models.Model):
    water = models.ForeignKey(
        Water, on_delete=models.CASCADE, related_name="water_logs"
    )
    intake = models.IntegerField()
    intaked_time = models.TimeField(auto_now_add=True)


class GidrationTip(models.Model):
    name = models.CharField(max_length=63)
    description = models.TextField()
    image = models.ImageField(upload_to=get_tip_image)
