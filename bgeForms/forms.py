from employee.models import Employee
from django import forms
from .models import FTE, ProcessedPaperSales


class DateInput(forms.DateInput):
    input_type = "date"


class FTEForm(forms.ModelForm):

    class Meta:
        model = FTE
        fields = "__all__"
        widgets = {
            "completion_time": forms.HiddenInput(),
            "head_count_date": DateInput(),
            "rsm_email": forms.HiddenInput(),
            "rsm_name": forms.HiddenInput(),
            "total_headcount": forms.HiddenInput(),
        }


class ProcessedPaperSalesForm(forms.ModelForm):

    class Meta:
        model = ProcessedPaperSales
        fields = "__all__"
        widgets = {
            "mprn": forms.Textarea(attrs={"rows": 2,
                                          "placeholder": "11111111111 22222222222"}),
            "gprn": forms.Textarea(attrs={"rows": 2,
                                          "placeholder": "1111111 2222222"}),
            "submitted_on": DateInput()
        }

    def __init__(self, team, *args, **kwargs):
        super(ProcessedPaperSalesForm, self).__init__(*args, **kwargs)
        self.fields['sales_agent'].queryset = Employee.objects.filter(
            department__department_name=team).exclude(
                employee_status="Leaver").order_by("first_name")
