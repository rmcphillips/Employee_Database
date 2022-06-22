from django import forms
from .models import DeviceAbstract, Phone, SIM, Tablet, OtherDevice
from employee.models import Employee
from django.db.models import Q


device_choices = (
    ("", ""),
    ("sim", "SIM"),
    ("phone", "Phone"),
    ("tablet", "Tablet"),
    ("other_device", "Other"),
)


class DeviceTypeForm(forms.Form):
    device_type = forms.ChoiceField(choices=device_choices,
                                    label="Device Type",
                                    required=True,
                                    help_text="Please select a device type \
                                        from the list")


class DeviceForm(forms.ModelForm):

    """Abstract form for devices."""
    class Meta:
        model = DeviceAbstract
        fields = ["status", "damaged", "serial_number", "assigned_to"]
        exclude = ["created_by"]

    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)

        self.fields['assigned_to'].queryset = Employee.objects.exclude(
            employee_status="Leaver").order_by("first_name")

        self.fields['acquisition_date'] = forms.DateField(
            widget=forms.DateInput(attrs={"type": "date"}))


class SIMForm(DeviceForm):

    """Abstract form for SIM."""
    class Meta:
        model = SIM
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["number"] = forms.CharField(
            widget=forms.TextInput(attrs={"placeholder": "0873334444"}))


class PhoneForm(DeviceForm):

    """Abstract form for Phone."""
    class Meta:
        model = Phone
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sim'].queryset = SIM.objects.filter(
            Q(assigned_to_id=None) |
            Q(assigned_to_id=self.instance.assigned_to_id))


class TabletForm(DeviceForm):

    """Abstract form for Tablet."""
    class Meta:
        model = Tablet
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sim'].queryset = SIM.objects.filter(
            Q(assigned_to_id=None) |
            Q(assigned_to_id=self.instance.assigned_to_id))


class OtherDeviceForm(DeviceForm):

    """Abstract form for other devices."""
    class Meta:
        model = OtherDevice
        fields = "__all__"
