from django.db import models
from userAccounts.models import CustomUser
from employee.models import SubDepartment, Department, JobRole


yesOrNo = (
    ("Y", "Yes"),
    ("N", "No"),
)


class UserRoles(models.Model):
    """ User roles are defined by this model. Defines relationship of user-employee roles """

    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, null=True)
    role = models.ForeignKey(JobRole, null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(
        Department, null=True, on_delete=models.SET_NULL, verbose_name="Account/Department")
    sub_department = models.ForeignKey(
        SubDepartment, null=True, on_delete=models.SET_NULL, verbose_name="Sub Department", blank=True)
    is_manager = models.CharField(
        choices=yesOrNo, null=True, default="N", max_length=10)

    def __str__(self):
        return self.user
