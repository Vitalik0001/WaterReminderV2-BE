from django.urls import path

from water_reminder_app.views import DashboardView, WaterView

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("water/", WaterView.as_view(), name="water")

]

app_name = "water_reminder_app"
