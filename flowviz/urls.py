from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'eflow/', views.eflow, name='eflow'),
    url(r'scenario/(?P<scenario_id>[0-9]+)/$', views.scenario, name='scenario'),
    url(r'scenario/(?P<scenario_id>[0-9]+)/raster/(?P<attribute>[a-zA-Z\-]+)/', views.dynamic_raster, name='scenario-dynamic-raster'),
    url(r'scenario/(?P<scenario_id>[0-9]+)/stats/', views.deficit_stats_plot, name='scenario-deficit-stats'),
    url(r'scenario/(?P<scenario_id>[0-9]+)/days/', views.deficit_days_plot, name='scenario-deficit-days'),
    url(r'scenario/(?P<scenario_id>[0-9]+)/average/', views.right_plot, name='scenario-average'),
    url(r'scenario/(?P<scenario_id>[0-9]+)/edit/', views.edit_scenario, name='scenario-edit'),
]
