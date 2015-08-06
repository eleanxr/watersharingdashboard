from django.forms import ModelForm
from models import Scenario, GradedFlowTarget, GradedFlowTargetElement

from django.forms.models import modelform_factory

class ScenarioForm(ModelForm):
    class Meta:
        model = Scenario
        fields = [
            'watershed',
            'name',
            'description',

            'source_type',

            'gage_data',
            'excel_data',
        ]
