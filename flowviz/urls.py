from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'(?P<target_id>[0-9]+)/$', views.target, name='target'),
    url(r'(?P<target_id>[0-9]+)/raster/(?P<attribute>[a-zA-Z\-]+)/', views.dynamic_raster, name='dynamic_raster'),
    url(r'(?P<target_id>[0-9]+)/stats/', views.deficit_stats_plot, name='deficit_stats'),
    url(r'(?P<target_id>[0-9]+)/days/', views.deficit_days_plot, name='deficit_days'),
    url(r'(?P<target_id>[0-9]+)/average/', views.right_plot, name='average'),
]