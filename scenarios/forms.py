from django import forms

from .models import Scenario, CyclicTarget, CyclicTargetElement

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

class ScenarioExcelForm(forms.ModelForm):
    class Meta:
        model = Scenario
        fields = [
            'excel_file',
            'sheet_name',
            'date_column_name',
            'attribute_column_name',
            'target_column_name',
        ]

class CyclicTargetForm(forms.ModelForm):
    class Meta:
        model = CyclicTarget
        fields = ["name", "description"]

CyclicTargetElementFormSet = forms.inlineformset_factory(
    CyclicTarget, CyclicTargetElement,
    fields = [
        "from_month",
        "from_day",
        "to_month",
        "to_day",
        "target_value",
    ]
)

