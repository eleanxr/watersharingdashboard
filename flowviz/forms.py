from django import forms

from models import Project, HUCRegion, GISLayer, ProjectScenarioRelationship

from scenarios.models import Scenario
from econ.models import CropMix

class ProjectScenarioRelationshipForm(forms.Form):
    scenario = forms.ModelChoiceField(
        queryset=Scenario.objects.order_by('name'),
        empty_label="Choose a scenario",
    )
class ProjectCropMixRelationshipForm(forms.Form):
    crop_mix = forms.ModelChoiceField(
        queryset=CropMix.objects.order_by('name'),
        empty_label="Choose a crop mix",
    )

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "watershed",
            "name",
            "description",
            "huc_scale",
            "show_project",
        ]

HUCRegionFormSet = forms.inlineformset_factory(
    Project, HUCRegion,
    fields = [
        "hucid",
    ]
)

GISLayerFormSet = forms.inlineformset_factory(
    Project, GISLayer,
    fields = [
        "name",
        "description",
        "url",
    ]
)
