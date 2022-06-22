from django import forms

tenants = (
    ("", ""),
    ("iber", "Iberdrola"),
    ("inm", "INM"),
    ("pin", "Pinergy"),
)


class DncApiForm(forms.Form):
    tenant = forms.ChoiceField(label="Tenants", choices=tenants, required=True)
    campaignID = forms.CharField(label="Campaign ID", required=True)
    customerContactNumber = forms.CharField(label="Customer Contact Numbers",
                                            required=True,
                                            help_text="You can input one \
                                     or more phone numbers separated by spaces.",
                                            widget=forms.Textarea(attrs={"rows": 2}))
