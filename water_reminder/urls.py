from django.urls import path

from water_reminder.views import DashboardView

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard")
]

app_name = "water_reminder"
