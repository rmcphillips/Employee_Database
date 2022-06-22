from django.db import models
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django_countries.fields import CountryField
from django.core.validators import (
    RegexValidator,
    EmailValidator,
    MaxValueValidator,
    MinValueValidator
)
from django.conf import settings

# Signals
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_delete


# Counties choice tuple
counties = (
    ('other', 'Other/Abroad'),
    ('carlow', 'Carlow'),
    ('cavan', 'Cavan'),
    ('clare', 'Clare'),
    ('cork', 'Cork'),
    ('donegal', 'Donegal'),
    ('dublin', 'Dublin'),
    ('galway', 'Galway'),
    ('kerry', 'Kerry'),
    ('kildare', 'Kildare'),
    ('kilkenny', 'Kilkenny'),
    ('laois', 'Laois'),
    ('leitrim', 'Leitrim'),
    ('limerick', 'Limerick'),
    ('longford', 'Longford'),
    ('louth', 'Louth'),
    ('mayo', 'Mayo'),
    ('meath', 'Meath'),
    ('monaghan', 'Monaghan'),
    ('offaly', 'Offaly'),
    ('roscommon', 'Roscommon'),
    ('sligo', 'Sligo'),
    ('tipperary', 'Tipperary'),
    ('waterford', 'Waterford'),
    ('westmeath', 'Westmeath'),
    ('wexford', 'Wexford'),
    ('wicklow', 'Wicklow')
)

# Gender choices tuple
gender = (
    ("M", "Male"),
    ("F", "Female"),
    ("NA", "Non Applicable")
)

# Payment type choices tuple
payroll = (
    ("F", "Fortnightly"),
    ("M", "Monthly"),
)

# Phone validator +123456789 up to 15 digits allowed.
phoneValidator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message=(
        "Phone number must be entered in the format '+123456789'. "
        "Up to 15 digits allowed."
    )
)


class Employee(models.Model):
    """ Employee Model. Contains all personal data related to employee """

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        ordering = ["first_name", "last_name"]

    # Personal details
    first_name = models.CharField(
        max_length=20, null=True, verbose_name="First Name")
    last_name = models.CharField(
        max_length=50, null=True, verbose_name="Last Name")
    dob = models.DateField(max_length=8, null=True,
                           verbose_name="Date of Birth")
    gender = models.CharField(max_length=20, choices=gender, null=True)
    nationality = CountryField(null=True)
    address = models.CharField(max_length=255, null=True)
    eircode = models.CharField(
        max_length=7, null=True, blank=True, verbose_name="Eircode")
    county = models.CharField(max_length=20, choices=counties, null=True)
    personal_phone = models.CharField(
        max_length=20,
        null=True
    )
    personal_email = models.EmailField(
        max_length=100,
        null=True,
        blank=True,
        validators=[EmailValidator]
    )
    work_phone = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    work_email = models.EmailField(
        max_length=100,
        null=True,
        blank=True,
        validators=[EmailValidator]
    )
    pps_no = models.CharField(max_length=15, null=True,
                              verbose_name="PPS Number"
                              )
    employee_status = models.CharField(
        max_length=20, null=True, default="Active", blank=True)

    # Job details
    role_start = models.DateField(
        max_length=8, null=True, verbose_name="Role Start Date"
    )
    payroll_type = models.CharField(max_length=20, choices=payroll, null=True)
    role = models.ForeignKey("JobRole", null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(
        "Department", null=True,
        on_delete=models.SET_NULL, verbose_name="Account/Department")
    sub_department = models.ForeignKey(
        "SubDepartment", null=True,
        on_delete=models.SET_NULL, verbose_name="Sub Department", blank=True)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    health_care = models.BooleanField(
        verbose_name="Laya Health Care", null=True)
    pension = models.BooleanField(verbose_name="Pension", null=True)

    # Next of Kin
    kin_first_name = models.CharField(
        max_length=20, null=True, verbose_name="First Name")
    kin_last_name = models.CharField(
        max_length=50, null=True, verbose_name="Last Name")
    kin_email = models.EmailField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Email",
        validators=[EmailValidator]
    )
    kin_phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Phone",
        validators=[phoneValidator]
    )
    kin_relationship = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Relationship")

    # Visa details
    visa_no = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Visa Number")
    visa_type = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Visa Type")
    visa_expiry = models.DateField(
        max_length=8, null=True, blank=True, verbose_name="Visa Expiry Date"
    )

    # Driving License details
    driving_license_number = models.CharField(
        verbose_name="Driving License Number",
        max_length=50,
        null=True,
        blank=True)
    driving_license_issue_date = models.DateField(
        verbose_name="License Issue Date", blank=True, null=True)
    driving_license_expiration_date = models.DateField(
        verbose_name="License Expiration Date", blank=True, null=True)
    driving_license_origin = CountryField(
        verbose_name="License Origin", null=True, blank=True)
    driving_license_penalty_points = models.IntegerField(
        verbose_name="Penalty Points", null=True, blank=True)
    driving_license_convictions = models.TextField(
        null=True,
        blank=True,
        max_length=900,
        verbose_name="Convictions")
    driving_license_medical_conditions = models.TextField(
        null=True,
        blank=True,
        max_length=900,
        verbose_name="Medical Conditions")
    driving_license_claims = models.TextField(
        null=True,
        blank=True,
        max_length=900,
        verbose_name="Claims")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class SubDepartment(models.Model):
    """ Subdepartments table. It relates to Department. """

    class Meta:
        verbose_name = "Sub Department"
        verbose_name_plural = "Sub Departments"
        ordering = ["sub_department_name"]

    sub_department_name = models.CharField(
        max_length=50, null=True, verbose_name="Sub-Department", blank=True
    )

    def __str__(self):
        return self.sub_department_name


class Department(models.Model):
    """ Department model. All departments are listed here """

    class Meta:
        verbose_name = "Account/Department"
        verbose_name_plural = "Accounts/Departments"
        ordering = ["department_name"]

    department_name = models.CharField(
        max_length=50, null=True, verbose_name="Account/Department", blank=True
    )

    def __str__(self):
        return self.department_name


class JobRole(models.Model):
    """ Job roles model. All roles are listed here """

    class Meta:
        verbose_name = "Job Role"
        verbose_name_plural = "Job Roles"
        ordering = ["role_name"]

    role_name = models.CharField(
        max_length=50, null=True, verbose_name="Role", blank=True
    )

    def __str__(self):
        return self.role_name


class EmployeeLeave(models.Model):
    """
    Employee leave model.
    All leaves stay here until employee is deleted.
    """

    class Meta:
        verbose_name = "Employee Leave"
        verbose_name_plural = "Employee Leaves"

    employee = models.ForeignKey(
        "Employee", null=True, on_delete=models.CASCADE)
    start_date = models.DateField(
        max_length=8, null=True, verbose_name="Leave Start Date"
    )
    end_date = models.DateField(
        max_length=8, null=True, verbose_name="Leave End Date", blank=True
    )
    leave_type = models.ForeignKey(
        "LeaveStatus", null=True,
        verbose_name="Leave Type", on_delete=models.SET_NULL)
    notes = models.TextField(null=True, blank=True,
                             max_length=900, verbose_name="Additional Notes")
    has_deduction = models.BooleanField(
        verbose_name="Clawback/Deductions",
        default=False,
        null=False,
        blank=False)

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name}"


class AttendanceStatus(models.Model):
    """ Attendance status to be used by employee. """

    class Meta:
        verbose_name = "Attendance Status"
        verbose_name_plural = "Attendance Status"
        ordering = ["status_name"]

    status_name = models.CharField(
        max_length=50, null=True, verbose_name="Status", blank=True
    )

    def __str__(self):
        return self.status_name


class LeaveStatus(models.Model):
    """ Leave status to be used by employee. """

    class Meta:
        verbose_name = "Leave Status"
        verbose_name_plural = "Leave Status"
        ordering = ["status_name"]

    status_name = models.CharField(
        max_length=60, null=True, verbose_name="Status", blank=True
    )

    def __str__(self):
        return self.status_name


class EmployeeAttendance(models.Model):
    """ Employee Attendance model. Has employee and attendance fields """

    class Meta:
        ordering = ["attendance_date"]
        verbose_name = "Employee Attendance"
        verbose_name_plural = "Employees Attendances"

        constraints = [
            models.UniqueConstraint(fields=["employee", "attendance_date"],
                                    name="unique_employee_attendance")
        ]

    employee = models.ForeignKey(
        "Employee", null=True, on_delete=models.CASCADE)
    attendance_date = models.DateField(
        max_length=8, null=True, verbose_name="Attendance Date"
    )
    status = models.ForeignKey(
        "AttendanceStatus", null=True,
        on_delete=models.SET_NULL,
        related_name="status")
    hours_worked = models.FloatField(
        verbose_name="Hours",
        null=True, validators=[
            MinValueValidator(0), MaxValueValidator(8)]
    )
    additional_status = models.ForeignKey(
        "AttendanceStatus", null=True,
        on_delete=models.SET_NULL,
        related_name="aditional_status", blank=True)
    additional_hours_worked = models.FloatField(
        verbose_name="Additional Status Hours",
        blank=True, null=True, validators=[
            MinValueValidator(0), MaxValueValidator(8)]
    )
    overtime_hours = models.FloatField(
        verbose_name="Overtime Hours",
        blank=True, null=True, validators=[
            MinValueValidator(0), MaxValueValidator(8)]
    )
    notes = models.TextField(null=True, blank=True,
                             max_length=900, verbose_name="Additional Notes")
    modified_date = models.DateField(auto_now_add=True, null=True)
    modified_by = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.employee}"


class EmployeeJobHistory(models.Model):
    """
    Employee Job History.
    Realates to Employee, Department, Role and Sub-Department tables

    Required fields: role_start, role, department, sub_department
    Optional fields: role_end
    """

    class Meta:
        verbose_name = "Employee Job History"
        verbose_name_plural = "Employees Job History"

    employee = models.ForeignKey(
        "Employee", null=True, on_delete=models.CASCADE)
    role_start = models.DateField(
        max_length=8, null=True, verbose_name="Role Start Date"
    )
    role_end = models.DateField(
        max_length=8, null=True, verbose_name="Role End Date", blank=True
    )
    role = models.ForeignKey("JobRole", null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(
        "Department", null=True,
        on_delete=models.SET_NULL, verbose_name="Account/Department")
    sub_department = models.ForeignKey(
        "SubDepartment", null=True, blank=False,
        on_delete=models.SET_NULL, verbose_name="Sub Department")


class EmployeeDocuments(models.Model):
    """
    Employee Documents. Realates to Employee table.
    Fields: employee, file_name, upload_date(auto generated)
    """

    class Meta:
        verbose_name = "Employee Documents"
        verbose_name_plural = "Employees Documents"

    employee = models.ForeignKey(
        "Employee", null=True, on_delete=models.CASCADE)
    file_name = models.FileField(null=True, blank=True)
    upload_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_name}"


class EmployeeHolidays(models.Model):
    """
    Employee Holidays. Realates to Employee table.
    Fields: employee, carry_over_hours, carry_over_expiry_date,
    total_current_holidays, modified_date
    """

    class Meta:
        verbose_name = "Employee Holidays"
        verbose_name_plural = "Employees Holidays"

    employee = models.ForeignKey(
        "Employee", on_delete=models.CASCADE, null=True)
    carry_over_hours = models.FloatField(
        blank=False, verbose_name="Carry Over Hours", default=0,
        validators=[MinValueValidator(0)],
        help_text="Must be entered in hours. Days are 7.5h")
    carry_over_expiry_date = models.DateField(
        max_length=8, verbose_name="Carry Over Expiry Date",
        blank=False)

    def __str__(self):
        return f"{self.employee}"


@receiver(pre_delete, sender=EmployeeDocuments)
def delete_image(sender, instance, **kwargs):
    """ Deletes file from the media folder before deletion from DB. """
    if instance.file_name:
        instance.file_name.delete(False)


@receiver(post_save, sender=EmployeeAttendance)
def attendanceUpdatedHandler(sender, instance, created, *args, **kwargs):
    """
    When new attendance is added updates the status
    of the employee to have the same status
    """

    employee = get_object_or_404(Employee, id=instance.employee.id)

    currentStatus = EmployeeAttendance.objects.filter(
        employee=employee).order_by("-attendance_date").first()

    employee.employee_status = str(currentStatus.status)
    employee.save()


@receiver(post_delete, sender=EmployeeAttendance)
def attendanceDeleteHandler(sender, instance, *args, **kwargs):
    """
    When new attendance is deleted updates the status
    of the employee to have the same status
    """

    employee = get_object_or_404(Employee, id=instance.employee.id)

    currentStatus = EmployeeAttendance.objects.filter(
        employee=employee).order_by("-attendance_date").first()

    if currentStatus:
        employee.employee_status = str(currentStatus.status)
        employee.save()


@receiver(post_save, sender=Employee)
def jobHistoryEmployeeHandler(sender, instance, created, *args, **kwargs):
    """
    When new employee is added updates the job history
    of the employee to have the same data.
    """
    if created:
        jobHistory = EmployeeJobHistory()

        jobHistory.employee = instance
        jobHistory.role_start = instance.role_start
        jobHistory.role = instance.role
        jobHistory.department = instance.department
        jobHistory.sub_department = instance.sub_department

        jobHistory.save()


@receiver(post_save, sender=EmployeeLeave)
def leaveUpdatedHandler(sender, instance, created, *args, **kwargs):
    """
    When new attendance is added updates the status
    of the employee to have the same status
    """

    employee = get_object_or_404(Employee, id=instance.employee.id)

    employee.employee_status = "Leaver"
    employee.save()
