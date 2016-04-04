from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect

from utils.views import BaseView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from datetime import datetime

from .forms import FileUploadForm

from models import DataFile

class UploadFile(BaseView):
    template = 'datafiles/upload_file.django.html'
    title = 'Upload File'

    def get(self, request):
        form = FileUploadForm()
        return render(request, self.template, self.get_context(
            title = self.title,
            form = form,
        ))

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
