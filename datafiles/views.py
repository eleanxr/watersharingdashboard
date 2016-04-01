from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from utils.views import BaseView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from datetime import datetime

from .forms import FileUploadForm

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
            return redirect("upload-complete", file_id=datafile.id)
        return render(request, self.template, self.get_context(
            title=self.title,
            form=form,
        ))
        
            
def upload_complete(request, file_id):
    return render(request, 'datafiles/upload_complete.django.html', {
        'title': 'Upload Complete!',
        'year': datetime.now().year,
    })