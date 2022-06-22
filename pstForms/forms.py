from django import forms
from .models import CECDisplay


class CECDisplayForm(forms.ModelForm):
    class Meta:
        model = CECDisplay
        fields = [
            "entry_type",
            "current",
            "target"
        ]
