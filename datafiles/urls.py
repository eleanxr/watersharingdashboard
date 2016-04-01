from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'upload', views.UploadFile.as_view(), name="upload-file"),
    url(r'upload-complete/(?P<file_id>[0-9]+)/$', views.upload_complete, name="upload-complete"),
]