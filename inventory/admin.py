from django.contrib import admin
from .models import OtherDevice, Phone, SIM, Tablet

# Register your models here.


class SIMAdmin(admin.ModelAdmin):
    list_display = [
        "assigned_to",
        "number",
        "serial_number"
    ]

    search_fields = [
        "number",
        "serial_number"
    ]


class PhoneAdmin(admin.ModelAdmin):
    list_display = [
        "assigned_to",
        "status",
        "location",
        "sim",
        "serial_number",
        "brand",
        "model",
    ]

    search_fields = [
        "status",
        "location",
        "sim__number",
        "serial_number",
        "brand",
        "model",
    ]


class TabletAdmin(admin.ModelAdmin):
    list_display = [
        "assigned_to",
        "status",
        "location",
        "sim",
        "serial_number",
        "brand",
        "model",
    ]

    search_fields = [
        "status",
        "location",
        "sim__number",
        "serial_number",
        "brand",
        "model",
    ]


class OtherDeviceAdmin(admin.ModelAdmin):
    list_display = [
        "assigned_to",
        "status",
        "location",
        "serial_number",
        "other_device_type"
    ]

    search_fields = [
        "status",
        "location",
        "serial_number",
        "other_device_type"
    ]


admin.site.register(SIM, SIMAdmin)
admin.site.register(Phone, PhoneAdmin)
admin.site.register(Tablet, TabletAdmin)
admin.site.register(OtherDevice, OtherDeviceAdmin)
