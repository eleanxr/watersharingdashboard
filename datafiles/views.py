from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

from utils.views import BaseView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from datetime import datetime

from .forms import FileUploadForm
from .serializers import DataFileSerializer

from models import DataFile

class UploadFile(BaseView):
    template = 'datafiles/upload_file.django.html'
    title = 'Upload File'

    @method_decorator(login_required)
    def get(self, request):
        form = FileUploadForm()
        return render(request, self.template, self.get_context(
            title = self.title,
            form = form,
        ))

    @method_decorator(login_required)
    def post(self, request):
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            datafile = form.save(commit=False)
            datafile.uploaded_by = request.user
            datafile.save()
            return redirect("view-file", file_id=datafile.id)
        return render(request, self.template, self.get_context(
            title=self.title,
            form=form,
        ))


def view_file(request, file_id):
    file = get_object_or_404(DataFile, pk=file_id)
    return render(request, 'datafiles/view_file.django.html', {
        'title': file.name,
        'description': file.description,
        'url': file.data_file.url,
        'year': datetime.now().year,
    })

class DataFileList(APIView):
    """REST API for listing and posting new datafiles."""
    parser_classes = (FormParser, MultiPartParser,)

    def get(self, request, format=None):
        files = DataFile.objects.all()
        serializer = DataFileSerializer(files, many=True)
        return Response(serializer.data)

    @method_decorator(login_required)
    def post(self, request, format=None):
        serializer = DataFileSerializer(data=request.data)
        if serializer.is_valid():
            datafile = serializer.save(uploaded_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
