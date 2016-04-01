from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'upload/$', views.UploadFile.as_view(), name="upload-file"),
    url(r'file/(?P<file_id>[0-9]+)/$', views.view_file, name="view-file"),
]