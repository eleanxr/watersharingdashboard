from django import forms

from .models import Scenario

class ScenarioForm(forms.ModelForm):
    class Meta:
        model = Scenario
        fields = [
            "name",
            "description",
            "attribute_multiplier",
            "source_type",
        ]

class ScenarioGageForm(forms.ModelForm):
    class Meta:
        model = Scenario
        fields = [
            "gage_location",
            "parameter_code",
            "parameter_name",
            "start_date",
            "end_date",
            "target",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={'class': 'datepicker'}),
            "end_date": forms.DateInput(attrs={"class": "datepicker"}),
        }

