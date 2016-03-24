from django.conf.urls import url

from . import views

urlpatterns = [
    #
    # Scenario views
    #

    url(r'scenario/(?P<scenario_id>[0-9]+)/$', views.scenario, name='scenario'),

    # Scenario
    url(r'scenario/(?P<scenario_id>[0-9]+)/raster/', views.dynamic_raster, name='scenario-dynamic-raster'),
    # Temporal Deficit Plots
    url(r'scenario/(?P<scenario_id>[0-9]+)/temporal_monthly/', views.deficit_days_plot, name='scenario-deficit-days'),
    url(r'scenario/(?P<scenario_id>[0-9]+)/temporal_annual/', views.annual_deficit_days_plot, name='scenario-deficit-days-annual'),
    # Volume Deficit Plots
    url(r'scenario/(?P<scenario_id>[0-9]+)/volume_monthly_pct/', views.deficit_stats_pct_plot, name='scenario-deficit-stats-pct'),
    url(r'scenario/(?P<scenario_id>[0-9]+)/volume_annual_pct/', views.deficit_stats_pct_plot_annual, name='scenario-deficit-stats-pct-annual'),
    url(r'scenario/(?P<scenario_id>[0-9]+)/volume_monthly/', views.deficit_stats_plot, name='scenario-deficit-stats'),
    url(r'scenario/(?P<scenario_id>[0-9]+)/volume_annual/', views.deficit_stats_plot_annual, name='scenario-deficit-stats-annual'),

    # Other Scenario URLs
    url(r'scenario/(?P<scenario_id>[0-9]+)/average/', views.right_plot, name='scenario-average'),
    url(r'scenario/(?P<scenario_id>[0-9]+)/data/', views.scenario_data, name='scenario-data'),
    url(r'scenario/(?P<scenario_id>[0-9]+)/annual_min/', views.long_term_minimum_plot, name='scenario-annual-min'),

    # Edit/create URLs
    url(r'scenario/(?P<scenario_id>[0-9]+)/edit/', views.scenario_edit, name='scenario-edit'),
]
