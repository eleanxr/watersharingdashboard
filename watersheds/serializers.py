from rest_framework import serializers

from .models import Watershed

class WatershedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watershed
        fields = ['name']
