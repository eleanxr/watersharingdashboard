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
            
            'flow_target',
            
            'gage_location',
            'start_date',
            'end_date',
            
            'flow_data_file',
            'date_column_name',
            'flow_column_name',
        ]
