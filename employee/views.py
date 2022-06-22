from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    Employee,
    EmployeeDocuments,
    EmployeeHolidays,
    EmployeeLeave,
    EmployeeAttendance,
    EmployeeJobHistory
)
from .forms import (
    EmployeeModelForm,
    EmployeeLeaveInlineForm,
    EmployeeJobHistoryInlineForm,
    EmployeeAttendanceInlineForm,
    EmployeeDocumentInlineForm,
    EmployeeHolidaysForm,
)
from inventory.models import Phone, Tablet, SIM, OtherDevice
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Value as V
from django.db.models.functions import Concat
from django.contrib import messages
from userRoles.views import getUserType, getSeniorManager
from userAccounts.models import CustomUser
import datetime
import math


def userHasAccess(user):

    if (getUserType(user) == "HR" or
            getUserType(user) == "manager" or
            user.is_superuser):
        return True
    else:
        return False


@login_required
@user_passes_test(userHasAccess,
                  login_url="/dashboard/",
                  redirect_field_name=None)
def employeeList(request):
    """ Renders a paginated list of all employees. """

    searchQuery = request.GET.get("searchEmployee", None)
    managerList = CustomUser.objects.filter(
        is_manager="Y").order_by("username")

    if searchQuery and searchQuery.isdigit():
        employees = Employee.objects.annotate(
            full_name=Concat('first_name', V(' '), 'last_name')
        ).filter(
            Q(full_name__icontains=searchQuery) |
            Q(last_name__icontains=searchQuery) |
            Q(first_name__icontains=searchQuery) |
            Q(work_email__icontains=searchQuery) |
            Q(role__role_name__icontains=searchQuery) |
            Q(department__department_name__icontains=searchQuery) |
            Q(sub_department__sub_department_name__icontains=searchQuery) |
            Q(employee_status__icontains=searchQuery) |
            Q(manager=searchQuery)
        ).order_by("first_name")

    elif searchQuery and not searchQuery.isdigit():
        employees = Employee.objects.annotate(
            full_name=Concat('first_name', V(' '), 'last_name')
        ).filter(
            Q(full_name__icontains=searchQuery) |
            Q(last_name__icontains=searchQuery) |
            Q(first_name__icontains=searchQuery) |
            Q(work_email__icontains=searchQuery) |
            Q(role__role_name__icontains=searchQuery) |
            Q(department__department_name__icontains=searchQuery) |
            Q(sub_department__sub_department_name__icontains=searchQuery) |
            Q(employee_status__icontains=searchQuery)
        ).order_by("first_name")

    else:
        employees = Employee.objects.all().order_by("first_name")

    if getUserType(request.user) == "manager" and not (
            getUserType(request.user) == "HR" or
            getSeniorManager(request.user) == "SFSM" or
            getSeniorManager(request.user) == "OPM" or
            getSeniorManager(request.user) == "ACD"):
        employees = employees.filter(
            manager=request.user
        ).exclude(
            employee_status="Leaver"
        )

    elif getSeniorManager(request.user) == "OPM":
        employees = employees.filter(
            department=request.user.department,
        ).exclude(
            employee_status="Leaver"
        )

    elif getSeniorManager(request.user) == "SFSM":
        employees = employees.filter(
            department=request.user.department,
            sub_department=request.user.sub_department
        ).exclude(
            employee_status="Leaver"
        )

    elif getSeniorManager(request.user) == "ACD":
        employees = employees.filter(
            department=request.user.department,
        ).exclude(
            employee_status="Leaver"
        )

    # Gives a list per page of 10 employees
    employeePaginator = Paginator(employees, 10)

    pageNum = (request.GET.get("page"))

    page = employeePaginator.get_page(pageNum)

    context = {
        "page": page,
        "managerList": managerList
    }

    return render(request, "employee/employeeList.html", context)


@ login_required
@ user_passes_test(userHasAccess,
                   login_url="/dashboard/",
                   redirect_field_name=None)
def employeeDetail(request, pk):
    """ Render employee details based on the PK/ID provided. """

    employee = get_object_or_404(Employee, id=pk)
    leaveList = EmployeeLeave.objects.filter(employee=employee)
    attendanceList = EmployeeAttendance.objects.filter(
        employee=employee).order_by("-attendance_date")[:60:-1]
    jobHistory = EmployeeJobHistory.objects.filter(employee=employee)
    documents = EmployeeDocuments.objects.filter(employee=employee)
    form = EmployeeModelForm(instance=employee)

    phones = Phone.objects.all().filter(assigned_to=pk)
    tablets = Tablet.objects.all().filter(assigned_to=pk)
    sims = SIM.objects.all().filter(assigned_to=pk)
    other_devices = OtherDevice.objects.all().filter(assigned_to=pk)

    annual_leave = calculate_annual_leave(employee)
    carry_over_holidays = EmployeeHolidays.objects.filter(
        employee=employee).first()

    holidays_form = EmployeeHolidaysForm(instance=carry_over_holidays)

    context = {
        "employee": employee,
        "leaveList": leaveList,
        "attendanceList": attendanceList,
        "jobHistory": jobHistory,
        "documents": documents,
        "form": form,
        "phones": phones,
        "tablets": tablets,
        "sims": sims,
        "other_devices": other_devices,
        "annual_leave": annual_leave,
        "holidays_form": holidays_form
    }
    return render(request, "employee/employeeDetail.html", context)


@ login_required
@ user_passes_test(userHasAccess,
                   login_url="/dashboard/",
                   redirect_field_name=None)
def employeeAddLeave(request, pk):
    """ Handles add/edit employee leave based on the PK/ID provided. """

    employee = get_object_or_404(Employee, id=pk)
    inlineForm = EmployeeLeaveInlineForm(instance=employee)

    # If request is POST, populate the inline form,
    # validates the form and save.
    if request.method == "POST":
        inlineForm = EmployeeLeaveInlineForm(request.POST, instance=employee)

        if inlineForm.is_valid():
            inlineForm.save()
            messages.success(request, "Employee leave updated successfully.")

            return redirect(f"/employee/{pk}")

        else:
            messages.error(request, "Error updating employee leave.")

    context = {
        "inlineForm": inlineForm,
        "employee": employee
    }
    return render(request, "employee/employeeLeave.html", context)


@ login_required
@ user_passes_test(userHasAccess,
                   login_url="/dashboard/",
                   redirect_field_name=None)
def employeeCreate(request):
    """
         Renders a new employee form and
         creates a new employee if form validation passes.
    """

    form = EmployeeModelForm()

    # If request is POST, validates the form and save.
    if request.method == "POST":

        form = EmployeeModelForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Employee created successfully.")

            return redirect("/employee")
        else:
            messages.error(request, form.errors)

    context = {
        "form": form
    }

    return render(request, "employee/employeeCreate.html", context)


@ login_required
@ user_passes_test(userHasAccess,
                   login_url="/dashboard/",
                   redirect_field_name=None)
def employeeUpdate(request, pk):
    """ Update an existing employee """

    employee = get_object_or_404(Employee, id=pk)
    form = EmployeeModelForm(instance=employee)
    carry_over_holidays = EmployeeHolidays.objects.filter(
        employee=employee).first()
    holidays_form = EmployeeHolidaysForm(instance=carry_over_holidays)
    annual_leave = calculate_annual_leave(employee)

    if request.method == "POST":

        form = EmployeeModelForm(request.POST, instance=employee)

        if form.is_valid():
            form.save()
            messages.success(request, "Employee updated successfully.")
            return redirect(f"/employee/{employee.id}")
        else:
            messages.error(
                request,
                ("Something went wrong. If the problem "
                 "persists contact support.")
            )

    context = {
        "employee": employee,
        "form": form,
        "annual_leave": annual_leave,
        "holidays_form": holidays_form,
        "carry_over_holidays": carry_over_holidays
    }

    return render(request, "employee/employeeUpdate.html", context)


@ login_required
@ user_passes_test(userHasAccess,
                   login_url="/dashboard/",
                   redirect_field_name=None)
def employeeDelete(request, pk):
    """ Delete an existing employee """

    try:
        employee = get_object_or_404(Employee, id=pk)
        employee.delete()
        messages.success(request, "Employee deleted successfully.")

    except Exception:
        messages.error(
            request,
            ("Sorry, something went wrong. "
             "If the problem persists contact support.")
        )

    finally:

        return redirect("/employee")


@ login_required
@ user_passes_test(userHasAccess,
                   login_url="/dashboard/",
                   redirect_field_name=None)
def employeeAddAttendance(request, pk):
    """ Handles Edit/Add attendance based on the PK/ID provided. """

    employee = get_object_or_404(Employee, id=pk)
    inlineForm = EmployeeAttendanceInlineForm(instance=employee)
    # If request is POST, populate the inline form,
    # validates the form and save.
    if request.method == "POST":
        inlineForm = EmployeeAttendanceInlineForm(
            request.POST, instance=employee)

        if inlineForm.is_valid():
            newInstances = inlineForm.save(commit=False)
            if newInstances:
                for newForm in newInstances:
                    newForm.modified_by = request.user.username
                    newForm.save()
            else:
                inlineForm.save()
            messages.success(request, "Attendance updated successfully.")

            return redirect(f"/employee/{pk}")
        else:
            messages.error(request, inlineForm.errors)
    context = {
        "inlineForm": inlineForm,
        "employee": employee
    }

    return render(request, "employee/employeeAttendance.html", context)


def deleteAttendance(request, pk):
    """ Delete an attendance entry """

    try:
        attendance = get_object_or_404(EmployeeAttendance, pk=pk)
        attendance.delete()
        messages.success(request, "Attendance deleted successfully.")

    except Exception:
        messages.error(
            request,
            ("Sorry, something went wrong. "
             "If the problem persists contact support.")
        )

    finally:

        return redirect(f"/employee/{attendance.employee.id}")


@ login_required
@ user_passes_test(userHasAccess,
                   login_url="/dashboard/",
                   redirect_field_name=None)
def updateTeamAttendance(request):
    """Updates team attendance"""

    # !This whole method needs to be refactored
    manager = request.user
    attendanceList = []

    team = Employee.objects.filter(
        manager=manager).exclude(employee_status="Leaver")

    teamActive = Employee.objects.filter(
        Q(manager=manager),
        Q(employee_status="Active") |
        Q(employee_status="Bank Holiday"))

    for emp in team:
        empAttendance = EmployeeAttendance.objects.filter(
            employee=emp).order_by("attendance_date").last()
        if empAttendance:
            attendanceList.append(empAttendance)

    inlineForm = EmployeeAttendanceInlineForm()

    if request.method == "POST":
        try:
            for e in teamActive:
                employee = get_object_or_404(Employee, id=e.pk)

                inlineForm = EmployeeAttendanceInlineForm(
                    request.POST, instance=employee)

                if inlineForm.is_valid():
                    newInstances = inlineForm.save(commit=False)
                    if newInstances:
                        for newForm in newInstances:
                            newForm.modified_by = request.user.username
                            inlineForm.save()
            messages.success(request, "Attendance updated successfully.")
            return redirect("/employee/attendance/")
        except(Exception):
            messages.error(request, "Something went wrong.")

    context = {
        "inlineForm": inlineForm,
        "team": team,
        "attendanceList": attendanceList
    }

    return render(request, "employee/updateTeamAttendance.html", context)


@ login_required
@ user_passes_test(userHasAccess,
                   login_url="/dashboard/",
                   redirect_field_name=None)
def employeeJobHistory(request, pk):
    """ Render employee leave based on the PK/ID provided. """

    employee = get_object_or_404(Employee, id=pk)
    inlineForm = EmployeeJobHistoryInlineForm(instance=employee)

    if request.method == "POST":
        inlineForm = EmployeeJobHistoryInlineForm(
            request.POST, instance=employee)

        if inlineForm.is_valid():
            inlineForm.save()
            messages.success(request, "Job history updated successfully.")

            return redirect(f"/employee/{pk}")
        else:
            messages.error(
                request, """Sorry, something went wrong.
                If the problem persists contact support.""")

    context = {
        "inlineForm": inlineForm,
        "employee": employee
    }

    return render(request, "employee/employeejobHistory.html", context)


@ login_required
@ user_passes_test(userHasAccess,
                   login_url="/dashboard/",
                   redirect_field_name=None)
def employeeUploadDocument(request, pk):
    """ Render Documents to employee. """

    employee = get_object_or_404(Employee, id=pk)
    inlineForm = EmployeeDocumentInlineForm(instance=employee)

    if request.method == "POST":
        inlineForm = EmployeeDocumentInlineForm(
            request.POST, request.FILES, instance=employee)

        if inlineForm.is_valid():
            inlineForm.save()
            messages.success(request, "Document updated successfully.")

            return redirect(f"/employee/{pk}/document")
        else:
            messages.error(
                request, """Sorry, something went wrong.
                If the problem persists contact support.""")
    context = {
        "inlineForm": inlineForm,
        "employee": employee
    }

    return render(request, "employee/employeeDocuments.html", context)


def update_carry_over_holidays(request, pk):
    """ Update the carry over holidays for an employee """

    employee_holiday = EmployeeHolidays.objects.filter(employee=pk).first()
    form = EmployeeHolidaysForm(instance=employee_holiday)

    if request.method == "POST":
        form = EmployeeHolidaysForm(request.POST, instance=employee_holiday)

        if form.is_valid():
            form.save()
            messages.success(
                request, "Carry over holidays updated successfully.")
            return redirect(f"/employee/{pk}")
        else:
            messages.error(
                request, """Sorry, something went wrong.
                If the problem persists contact support.""")
    context = {
        "form": form,
        "employee_id": pk,
        "employee_holiday": employee_holiday
    }

    return render(request,
                  "employee/includes/employeeHolidaysForm.html/", context)


def calculate_extra_holiday(employee: Employee):
    """
    Calculates the number of years worked by an employee.
    And returns a number of extra days off from 0 to 5.
    """

    job_history = EmployeeJobHistory.objects.filter(employee=employee)
    extra_holiday_allowance = 0
    today = datetime.date.today()

    for job in job_history:
        start_date = job.role_start
        end_date = job.role_end

        if end_date is None:
            end_date = today

        extra_holiday_allowance += (end_date - start_date).days / 365

    extra_holiday_allowance = math.floor(extra_holiday_allowance)

    # If paid forthnightly, calculates % based on hours worked.
    if employee.payroll_type == "F":
        if extra_holiday_allowance == 1:
            return 0.084
        elif extra_holiday_allowance == 2:
            return 0.088
        elif extra_holiday_allowance == 3:
            return 0.092
        elif extra_holiday_allowance == 4:
            return 0.096
        elif extra_holiday_allowance >= 5:
            return 0.1
        else:
            return 0.08

    elif employee.payroll_type == "M":
        return (37.5 if (extra_holiday_allowance * 7.5) > 37.5
                else (extra_holiday_allowance * 7.5))


def calculate_annual_leave(employee: Employee):
    """ Calculates the annual leave for an employee. """

    payable_holidays = get_payable_holidays(employee)
    holidays_taken = get_total_holidays_taken(employee)
    carry_over_holidays = get_carry_over_holidays(employee)

    current_holidays = ((payable_holidays - holidays_taken) +
                        carry_over_holidays)

    return round(current_holidays, 2)


def get_payable_holidays(employee: Employee):
    """ Returns the total hours of payable holidays for an employee. """

    current_year = datetime.date.today().year
    extra_holiday_allowance = calculate_extra_holiday(employee)
    total_hours_worked = 0
    holiday_allowance = 0

    if employee.payroll_type == "F":

        payable_attendance = EmployeeAttendance.objects.filter(
            Q(employee=employee) &
            Q(attendance_date__year=current_year) &
            (Q(status__status_name="Active") |
             Q(status__status_name="Inactive paid") |
             Q(status__status_name="Holidays") |
             Q(status__status_name="Maternity Leave") |
             Q(status__status_name="LTA") |
             Q(status__status_name="Bank Holiday") |
             Q(status__status_name="Induction"))
        )

        for a in payable_attendance:
            if (a.additional_status == ("Active" or
                                        "Inactive Paid" or
                                        "Holidays" or
                                        "Maternity Leave" or
                                        "LTA" or
                                        "Bank Holiday" or
                                        "Induction")):

                total_hours_worked += (a.hours_worked +
                                       a.additional_hours_worked +
                                       a.overtime_hours)
            else:
                total_hours_worked += (
                    (0 if a.hours_worked is None else a.hours_worked) +
                    (0 if a.overtime_hours is None else a.overtime_hours))

        holiday_allowance = total_hours_worked * extra_holiday_allowance

    elif employee.payroll_type == "M":
        holiday_allowance = 150 + extra_holiday_allowance

    return holiday_allowance


def get_total_holidays_taken(employee: Employee):
    """ Returns the total hours of holidays taken for an employee. """

    current_year = datetime.date.today().year
    total_holidays_taken = 0

    payable_attendance = EmployeeAttendance.objects.filter(
        Q(employee=employee) &
        Q(attendance_date__year=current_year) &
        (Q(status__status_name="Holidays"))
    )

    for a in payable_attendance:
        if a.additional_status == ("Holidays"):
            total_holidays_taken += (a.hours_worked +
                                     a.additional_hours_worked)
        else:
            total_holidays_taken += (0 if a.hours_worked is None
                                     else a.hours_worked)

    return total_holidays_taken


def get_carry_over_holidays(employee: Employee):
    """Returns carried over holidays from the last 6 months."""

    today = datetime.date.today()

    holidays = EmployeeHolidays.objects.filter(
        Q(employee=employee) &
        Q(carry_over_expiry_date__gte=today)
    ).first()

    if holidays:
        return holidays.carry_over_hours
    else:
        return 0
