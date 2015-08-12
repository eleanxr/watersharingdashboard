from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'projects/$', views.projects, name='projects'),
    url(r'projects/(?P<project_id>[0-9]+)/$', views.project_detail, name='project_detail'),
    url(r'projects/(?P<project_id>[0-9]+)/compare/$', views.project_compare, name='project_compare'),
    url(r'projects/(?P<project_id>[0-9]+)/compare/pct_plot$', views.project_deficit_days_plot, name='project_pct_plot'),
    url(r'projects/(?P<project_id>[0-9]+)/data/$', views.project_data, name='project_data'),
    url(r'projects/(?P<project_id>[0-9]+)/csv/$', views.project_data_csv, name='project_data_csv'),

    url(r'scenario/(?P<scenario_id>[0-9]+)/$', views.scenario, name='scenario'),
    url(r'scenario/(?P<scenario_id>[0-9]+)/raster/(?P<attribute>[a-zA-Z_\-]+)/', views.dynamic_raster, name='scenario-dynamic-raster'),
    url(r'scenario/(?P<scenario_id>[0-9]+)/stats/', views.deficit_stats_plot, name='scenario-deficit-stats'),
    url(r'scenario/(?P<scenario_id>[0-9]+)/days/', views.deficit_days_plot, name='scenario-deficit-days'),
    url(r'scenario/(?P<scenario_id>[0-9]+)/average/', views.right_plot, name='scenario-average'),
    url(r'scenario/(?P<scenario_id>[0-9]+)/data/', views.scenario_data, name='scenario-data'),
]
