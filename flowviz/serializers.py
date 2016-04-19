from rest_framework import serializers

from .models import ProjectScenarioRelationship, ProjectCropMixRelationship

class ProjectScenarioRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectScenarioRelationship
        fields = ['project', 'scenario',]

class ProjectCropMixRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCropMixRelationship
        fields = 'project', 'crop_mix'
