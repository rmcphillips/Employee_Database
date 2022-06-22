from django.urls import path
from .views import (attendance_report,
                    report_list,
                    draw_attendance_report,
                    leaver_report,
                    draw_leaver_report)

app_name = "reports"

urlpatterns = [
    path("report_list/", report_list, name="report_list"),
    path("attendance_report/", attendance_report, name="attendance_report"),
    path("leaver_report/", leaver_report, name="leaver_report"),
    path("draw_attendance_report/", draw_attendance_report,
         name="draw_attendance_report"),
    path("draw_leaver_report/", draw_leaver_report,
         name="draw_leaver_report"),
]
