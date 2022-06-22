from django.urls import path
from .views import managerList, managerUpdate

app_name = "userRoles"

urlpatterns = [
    path("", managerList, name="managerList"),
    path("<int:pk>/update/", managerUpdate, name="managerUpdate"),
]
