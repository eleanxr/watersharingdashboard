from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'upload/$', views.UploadFile.as_view(), name="upload-file"),
    url(r'file/(?P<file_id>[0-9]+)/$', views.view_file, name="view-file"),
    url(r'file/(?P<file_id>[0-9]+)/edit$', views.EditFile.as_view(), name="edit-file"),
    url(r'files/$', views.DataFileList.as_view(), name="list-files"),
]
