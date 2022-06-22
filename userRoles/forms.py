from django import forms
from userAccounts.models import CustomUser


class UserRolesModelForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "role",
            "department",
            "sub_department",
            "is_manager"
        ]
        widgets = {
            "username": forms.TextInput(attrs={"readonly": "True"})
        }

        help_texts = {
            "username": None
        }
