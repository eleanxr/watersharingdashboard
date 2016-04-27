from django import forms

from .models import DataFile

class FileUploadForm(forms.ModelForm):
    """Reusable form for uploading files and tracking the owner of the file.
    """
    class Meta:
        model = DataFile
        fields = [
            'data_file',
            'name',
            'description',
            'longitude',
            'latitude',
        ]
