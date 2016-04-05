from django import forms

from .models import Project, HUCRegion, GISLayer, ProjectScenarioRelationship

from scenarios.models import Scenario

class ProjectScenarioRelationshipForm(forms.Form):
    scenario = forms.ModelChoiceField(
        queryset=Scenario.objects.order_by('name'),
        empty_label="Choose a scenario",
    )
