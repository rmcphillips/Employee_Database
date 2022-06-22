from django.urls import path
from .views import cecDisplayForm, cecDisplay, getChartData

app_name = "iberForms"

urlpatterns = [
    path("forms/", cecDisplayForm, name="cecDisplayForm"),
    path("display/", cecDisplay, name="cecDisplay"),
    path("chart/", getChartData.as_view(), name="getChartData"),
]
