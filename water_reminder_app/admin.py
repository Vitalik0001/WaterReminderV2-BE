from django.contrib import admin

from water_reminder_app.models import (
    Water,
    WaterLog,
    GidrationTip
)

admin.site.register(Water)
admin.site.register(WaterLog)
admin.site.register(GidrationTip)
