from django import forms

from models import Project, HUCRegion, GISLayer, ProjectScenarioRelationship

from scenarios.models import Scenario

class ProjectScenarioRelationshipForm(forms.Form):
    scenario = forms.ModelChoiceField(
        queryset=Scenario.objects.order_by('name'),
        empty_label="Choose a scenario",
    )

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "watershed",
            "name",
            "description",
            "huc_scale",
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
