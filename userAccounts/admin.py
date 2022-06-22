from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "username",
        "email",
        "role",
        "department",
        "sub_department",
        "is_superuser",
        "is_staff",
        "is_manager",
    ]

    ordering = [
        "username"
    ]


admin.site.register(CustomUser, CustomUserAdmin)
