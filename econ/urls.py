from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'crops/(?P<crop_mix_id>[0-9]+)/$', views.crop_mix_detail, name='crop_mix_detail'),
    url(r'crops/(?P<crop_mix_id>[0-9]+)/download_area$', views.download_crop_mix_area_data, name='download_crop_mix_area'),
    
    url(r'crops/(?P<object_id>[0-9]+)/edit$', views.EditCropMixView.as_view(), name='crop_mix_edit'),
    url(r'crops/(?P<crop_mix_id>[0-9]+)/edit_groups$', views.EditCropMixGroupsView.as_view(), name='crop_mix_group_edit'),

    url(r'crops/new', views.NewCropMixView.as_view(), name="new-crop-mix"),
]
