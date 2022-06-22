from django.contrib import admin
from .models import FTE, ProcessedPaperSales


# Register your models here.

class FTEFormAdmin(admin.ModelAdmin):
    ordering = ["id"]

    list_display = [field.name for field in FTE._meta.get_fields()]


admin.site.register(FTE, FTEFormAdmin)
admin.site.register(ProcessedPaperSales)
