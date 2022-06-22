from django.contrib import admin
from rangefilter.filters import DateRangeFilter
from .models import (
    Employee,
    Department,
    EmployeeHolidays,
    JobRole,
    EmployeeLeave,
    EmployeeAttendance,
    AttendanceStatus,
    SubDepartment,
    EmployeeJobHistory,
    LeaveStatus,
    EmployeeDocuments
)


class EmployeeAttendanceAdmin(admin.ModelAdmin):
    list_display = [
        "employee",
        "status",
        "attendance_date",
        "modified_by"
    ]

    ordering = [
        "attendance_date"
    ]

    search_fields = [
        "employee__first_name",
        "employee__last_name",
        "attendance_date"
    ]

    list_filter = (("attendance_date", DateRangeFilter),
                   "status", "employee__department")


class EmployeeLeaveAdmin(admin.ModelAdmin):
    list_display = [
        "employee",
        "start_date",
        "end_date",
        "leave_type"
    ]

    ordering = ["employee"]


class EmployeeAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "__str__",
        "department",
        "sub_department",
        "manager"
    ]

    search_fields = [
        "department__department_name",
        "sub_department__sub_department_name",
        "work_email",
        "first_name",
        "last_name"
    ]

    list_filter = ["department", "sub_department"]


class EmployeeHolidaysAdmin(admin.ModelAdmin):
    list_display = [
        "employee",
        "carry_over_hours",
        "carry_over_expiry_date"
    ]

    ordering = ["employee"]


# Register your models here.
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeDocuments)
admin.site.register(Department)
admin.site.register(SubDepartment)
admin.site.register(JobRole)
admin.site.register(EmployeeJobHistory)
admin.site.register(EmployeeLeave, EmployeeLeaveAdmin)
admin.site.register(EmployeeAttendance, EmployeeAttendanceAdmin)
admin.site.register(AttendanceStatus)
admin.site.register(LeaveStatus)
admin.site.register(EmployeeHolidays, EmployeeHolidaysAdmin)
