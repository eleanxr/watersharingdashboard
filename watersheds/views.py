from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import generics

from .models import Watershed
from .serializers import WatershedSerializer

class ListWatershedsAPIView(generics.ListCreateAPIView):
    queryset = Watershed.objects.all()
    serializer_class = WatershedSerializer
