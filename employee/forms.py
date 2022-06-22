from django import forms
from django.forms.models import inlineformset_factory
from .models import (
    Employee,
    EmployeeDocuments,
    EmployeeLeave,
    EmployeeAttendance,
    EmployeeJobHistory,
    EmployeeHolidays
)

from django.contrib.auth import get_user_model

User = get_user_model()


class DateInput(forms.DateInput):
    input_type = "date"


class EmployeeAttendanceModelForm(forms.ModelForm):
    class Meta:
        model = EmployeeAttendance
        fields = [
            "employee",
            "attendance_date",
            "status",
            "hours_worked",
            "additional_status",
            "additional_hours_worked",
            "overtime_hours",
            "notes",
            "modified_by"
        ]
        widgets = {
            # Change fields to date field
            "attendance_date": DateInput(),
            "notes": forms.Textarea(attrs={"rows": 4})
        }

    def __init__(self, *args, **kwargs):
        super(EmployeeAttendanceModelForm, self).__init__(*args, **kwargs)

        # Change the step of the hours field to .5
        self.fields["hours_worked"].widget.attrs.update(
            {'step': "0.5", "min": 0})
        self.fields[
            "additional_hours_worked"
        ].widget.attrs.update({
            'step': "0.5", "min": 0})
        self.fields["overtime_hours"].widget.attrs.update({
            'step': "0.5", "min": 0})


# Inline Attendance Form
EmployeeAttendanceInlineForm = inlineformset_factory(
    Employee, EmployeeAttendance,
    form=EmployeeAttendanceModelForm,
    extra=1,)


class EmployeeLeaveModelForm(forms.ModelForm):
    class Meta:
        model = EmployeeLeave
        fields = [
            "start_date",
            "end_date",
            "leave_type",
            "has_deduction",
            "notes"
        ]

        widgets = {
            # Change fields to date field
            "start_date": DateInput(),
            "end_date": DateInput(),
            "notes": forms.Textarea(attrs={"rows": 4})
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError(
                    "End date cannot be earlier than start date!",
                    code="invalid")
        return cleaned_data


# Inline Leave Form
EmployeeLeaveInlineForm = inlineformset_factory(
    Employee, EmployeeLeave,
    form=EmployeeLeaveModelForm,
    extra=1,
    widgets={
        # Change fields to date field
        "start_date": DateInput(),
        "end_date": DateInput(),
        "notes": forms.Textarea(attrs={"rows": 4})
    })


class EmployeeModelForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"
        widgets = {
            # Change fields to date field
            "dob": DateInput(),
            "role_start": DateInput(),
            "visa_expiry": DateInput(),
            "driving_license_issue_date": DateInput(),
            "driving_license_expiration_date": DateInput(),
            "driving_license_convictions": forms.Textarea(attrs={"rows": 2}),
            "driving_license_medical_conditions": forms.Textarea(attrs={"rows": 2}),
            "driving_license_claims": forms.Textarea(attrs={"rows": 2})
        }

    def __init__(self, *args, **kwargs):
        managerList = User.objects.filter(is_manager="Y")

        super(EmployeeModelForm, self).__init__(*args, **kwargs)

        self.fields["manager"] = forms.ModelChoiceField(
            queryset=managerList, required=False)


class EmployeeJobHistoryModelForm(forms.ModelForm):
    class Meta:
        model = EmployeeJobHistory
        fields = [
            "role_start",
            "role_end",
            "role",
            "department",
            "sub_department"
        ]

        widgets = {
            # Change fields to date field
            "role_start": DateInput(),
            "role_end": DateInput()
        }

    def clean(self):
        cleaned_data = super().clean()
        role_start = cleaned_data.get("role_start")
        role_end = cleaned_data.get("role_end")

        if role_start and role_end:
            if role_end < role_start:
                raise forms.ValidationError(
                    "End date cannot be earlier than start date!",
                    code="invalid")
        return cleaned_data


# Inline Job History Form
EmployeeJobHistoryInlineForm = inlineformset_factory(
    Employee, EmployeeJobHistory,
    form=EmployeeJobHistoryModelForm,
    extra=1,
)


# Inline Documents Form
EmployeeDocumentInlineForm = inlineformset_factory(
    Employee, EmployeeDocuments,
    fields=(
        "file_name",
    ),
    extra=1,
)


class EmployeeHolidaysForm(forms.ModelForm):
    class Meta:
        model = EmployeeHolidays
        fields = [
            "carry_over_hours",
            "carry_over_expiry_date"
        ]

        widgets = {
            # Change fields to date field
            "carry_over_expiry_date": DateInput()
        }

    def __init__(self, *args, **kwargs):
        super(EmployeeHolidaysForm, self).__init__(*args, **kwargs)

        # Change the step of the hours field to .5
        self.fields["carry_over_hours"].widget.attrs.update(
            {'step': "0.5", "min": 0})
