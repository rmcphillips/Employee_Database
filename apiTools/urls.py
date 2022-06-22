from django.urls import path
from . import views

app_name = "apiTools"

urlpatterns = [
    path("dncApi/", views.dncApi, name="dncApi"),
    path("dncApiExportCSV/", views.dncApiExportCSV, name="dncApiExportCSV"),
    path("dncApiExportXLS/", views.dncApiExportXLS, name="dncApiExportXLS"),
]
