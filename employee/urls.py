from django.urls import path
from .views import (
    employeeList,
    employeeDetail,
    employeeCreate,
    employeeUpdate,
    employeeDelete,
    employeeAddLeave,
    employeeAddAttendance,
    employeeJobHistory,
    updateTeamAttendance,
    employeeUploadDocument,
    deleteAttendance,
    update_carry_over_holidays
)

app_name = "employee"

urlpatterns = [
    path("", employeeList, name="employeeList"),
    path("<int:pk>/", employeeDetail, name="employeeDetail"),
    path("create/", employeeCreate, name="employeeCreate"),
    path("<int:pk>/update/", employeeUpdate, name="employeeUpdate"),
    path("<int:pk>/delete/", employeeDelete, name="employeeDelete"),
    path("<int:pk>/leave/", employeeAddLeave, name="employeeAddLeave"),
    path(
        "<int:pk>/jobHistory/",
        employeeJobHistory,
        name="employeeJobHistory"
    ),
    path(
        "<int:pk>/document/",
        employeeUploadDocument,
        name="employeeUploadDocument"
    ),
    path("<int:pk>/attendance/", employeeAddAttendance,
         name="employeeAddAttendance"),
    path("<int:pk>/deleteAttendance/", deleteAttendance,
         name="deleteAttendance"),
    path("attendance/", updateTeamAttendance,
         name="updateTeamAttendance"),
    path("<int:pk>/update_carry_over_holidays/", update_carry_over_holidays,
         name="update_carry_over_holidays"),
]
