from django.core.validators import (MaxLengthValidator,
                                    MinLengthValidator, MinValueValidator)
from django.db import models
from employee.models import Employee
from userAccounts.models import CustomUser


device_status = (
    ("active", "Active"),
    ("inactive", "Inactive"),
    ("out_of_order", "Out of Order"),
    ("repair", "Repair"),
)

location_choices = (
    ("cec1", "CEC-1"),
    ("cec2", "CEC-2"),
    ("field", "Field"),
    ("galway", "Galway"),
    ("other", "Other")
)

other_devices_list = (
    ("laptop", "Laptop"),
    ("desktop", "Desktop"),
    ("mouse", "Mouse"),
    ("keyboard", "Keyboard"),
    ("docker", "Docker"),
    ("power_bank", "Powerbank"),
    ("headset", "Headset"),
    ("4g_modem", "4G Modem"),
    ("other", "Other"),
)


class DeviceAbstract(models.Model):
    """Abstract model for all devices"""

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, editable=False)
    assigned_to = models.ForeignKey(
        Employee, on_delete=models.SET_NULL,
        null=True,
        verbose_name="Assign to Employee",
        blank=True)
    serial_number = models.CharField(
        max_length=255, unique=True, blank=False, verbose_name="Serial Number")
    status = models.CharField(
        max_length=20, choices=device_status, verbose_name="Status")
    location = models.CharField(
        choices=location_choices,
        max_length=20, verbose_name="Location", null=True)
    damaged = models.BooleanField(
        verbose_name="Damaged", null=True, default=False)
    transit = models.BooleanField(
        verbose_name="In Transit", null=True, default=False)
    acquisition_date = models.DateField(
        blank=True, null=True, verbose_name="Acquisition Date")

    class Meta:
        abstract = True


class SIM(DeviceAbstract):
    """Model for SIM cards"""

    number = models.CharField(
        max_length=255, blank=False, verbose_name="Number")

    def __str__(self):
        return self.number


class Phone(DeviceAbstract):
    """Model for phones"""

    sim = models.OneToOneField(SIM, on_delete=models.SET_NULL,
                               null=True, verbose_name="SIM",
                               unique=True, blank=True,
                               )
    imei = models.CharField(unique=True, blank=False,
                            max_length=16,
                            verbose_name="IMEI",
                            validators=[MinLengthValidator(14),
                                        MaxLengthValidator(16)])
    brand = models.CharField(max_length=255, blank=False, verbose_name="Brand")
    model = models.CharField(max_length=255, blank=False, verbose_name="Model")

    def __str__(self):
        return self.imei


class Tablet(DeviceAbstract):
    tablet_name = models.CharField(max_length=255, blank=False,
                                   verbose_name="Tablet Name")
    sim = models.OneToOneField(SIM, on_delete=models.CASCADE,
                               null=True, verbose_name="SIM",
                               unique=True, blank=True)
    imei = models.CharField(unique=True, blank=False,
                            max_length=16,
                            verbose_name="IMEI",
                            validators=[MinLengthValidator(14),
                                        MaxLengthValidator(16)])
    brand = models.CharField(max_length=255, blank=False, verbose_name="Brand")
    model = models.CharField(max_length=255, blank=False, verbose_name="Model")

    def __str__(self):
        return self.tablet_name


class OtherDevice(DeviceAbstract):
    """Model for Other devices"""

    other_device_type = models.CharField(
        max_length=255, blank=False,
        choices=other_devices_list,
        verbose_name="Device Type")
    workstation = models.IntegerField(
        verbose_name="Workstation Number", null=True,
        blank=True, validators=[MinValueValidator(1)])

    def __str__(self):
        return self.other_device_type
