from django.urls import path
from .views import dashboard, getChartData

app_name = "dashboard"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("chart/", getChartData.as_view(), name="getChartData"),
]
