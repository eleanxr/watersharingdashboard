from django.forms import ModelForm
from models import Scenario, GradedFlowTarget, GradedFlowTargetElement
from models import GageDataSource, ExcelDataSource, DataFile

from django.forms.models import modelform_factory

class ScenarioForm(ModelForm):
    class Meta:
        model = Scenario
        fields = [
            'watershed',
            'name',
            'description',

            'source_type',
        ]

class GageDataSourceForm(ModelForm):
    class Meta:
        model = GageDataSource
        fields = [
            'gage_location',
            'start_date',
            'end_date',
            'graded_flow_target',
        ]

class ExcelDataSourceForm(ModelForm):
    class Meta:
        model = ExcelDataSource
        fields = [
            'excel_file',
            'sheet_name',
            'date_column_name',
            'flow_column_name',
            'target_column_name',
        ]
