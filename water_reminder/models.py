from django.conf import settings
from django.db import models
from django.utils import timezone


class Water(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="waters"
    )
    total_intake = models.IntegerField(default=0)
    daily_intake = models.IntegerField(default=0)
    average_intake = models.IntegerField(default=0.0)
    intake_goal = models.IntegerField(default=0)
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
