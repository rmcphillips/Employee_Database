from django.contrib import admin
from .models import UserRoles


class UserRoleAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "is_manager",
        "role",
        "department",
        "sub_department"
    ]


# Register your models here.
admin.site.register(UserRoles, UserRoleAdmin)
