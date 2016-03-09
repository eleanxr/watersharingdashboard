from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'crops/(?P<crop_mix_id>[0-9]+)/$', views.crop_mix_detail, name='crop_mix_detail'),
]
