from django import forms
from employee.models import Department, Employee

payroll = (
    ("F", "Fortnightly"),
    ("M", "Monthly"),
)


class AttendanceReportForm(forms.Form):
    """ Form to get the attendance report for payroll. """

    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.all(), required=False)
    department = forms.ModelChoiceField(
        Department.objects.all(), required=False)
    payroll_type = forms.ChoiceField(choices=payroll, required=True)


class LeaverReportForm(forms.Form):
    """ Form to get the attendance report for payroll. """

    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.all(), required=False)
    department = forms.ModelChoiceField(
        Department.objects.all(), required=False)
