from rest_framework import serializers

from .models import ProjectScenarioRelationship

class ProjectScenarioRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectScenarioRelationship
        fields = ['project', 'scenario',]
