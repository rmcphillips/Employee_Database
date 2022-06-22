from django.db import models
from django.contrib.auth.models import AbstractUser
from employee.models import SubDepartment, Department, JobRole

# Create your models here.
yesOrNo = (
    ("Y", "Yes"),
    ("N", "No"),
)


class CustomUser(AbstractUser):
    role = models.ForeignKey(JobRole, null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(
        Department, null=True, on_delete=models.SET_NULL, verbose_name="Account/Department")
    sub_department = models.ForeignKey(
        SubDepartment, null=True, on_delete=models.SET_NULL, verbose_name="Sub Department", blank=True)
    is_manager = models.CharField(
        choices=yesOrNo, null=True, default="N", max_length=10)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
