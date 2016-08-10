from django import forms

from .models import Scenario, CyclicTargetElement

class ScenarioForm(forms.ModelForm):
    class Meta:
        model = Scenario
        fields = [
            # Common fields
            "name",
            "description",
            "attribute_multiplier",
            "drought_exceedance",
            "source_type",
            "critical_season_begin",
            "critical_season_end",
            "crop_mix",
            "instream_flow_rights",

            # Gage fields
            "gage_location",
            "parameter_code",
            "parameter_name",
            "start_date",
            "end_date",

            # Excel fields
            'excel_file',
            'sheet_name',
            'date_column_name',
            'attribute_column_name',
            'target_column_name',
        ]

        widgets = {
            # Use jQuery date pickers for the start and end dates.
            "start_date": forms.DateInput(attrs={'class': 'datepicker'}),
            "end_date": forms.DateInput(attrs={"class": "datepicker"}),
        }

CyclicTargetElementFormSet = forms.inlineformset_factory(
    Scenario, CyclicTargetElement,
    fields = [
        "from_month",
        "from_day",
        "to_month",
        "to_day",
        "target_value",
    ]
)
