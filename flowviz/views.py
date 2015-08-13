from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.core import serializers

from models import Project, Scenario

from waterkit import plotting, analysis

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from pylab import figure
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.colors

import pandas as pd

def index(request):
    return render(request, 'flowviz/index.django.html')

def projects(request):
    projects = Project.objects.all().order_by('name')
    return render(request, 'flowviz/projects.django.html',{
        'projects': projects,
    })

def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    context = {
        'project': project,
    }
    return render(request, 'flowviz/project.django.html', context)

def project_compare(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    context = {
        'project': project,
    }
    return render(request, 'flowviz/project_compare.django.html', context)

def __get_deficit_days_comparison(project):
    datasets = []
    names = []
    for scenario in project.scenario_set.all():
        data = scenario.get_data()
        attribute_name = scenario.get_gap_attribute_name()
        data_pct = analysis.deficit_pct(data, attribute_name, 'month')
        names.append(scenario.name)
        datasets.append(data_pct)
    return analysis.compare_datasets(datasets, 'pct', names)

def __get_deficit_stats_comparison(project):
    datasets = []
    names = []
    for scenario in project.scenario_set.all():
        data = scenario.get_data()
        attribute_name = scenario.get_gap_attribute_name()
        names.append(scenario.name)
        datasets.append(data[data[attribute_name] < 0].groupby('month').median())
    return analysis.compare_datasets(datasets, attribute_name, names)

def project_data(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    result = __get_deficit_days_comparison(project)
    response = HttpResponse(content_type="application/json")
    result.to_json(response, orient='index')
    return response

def project_deficit_days_csv(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    result = __get_deficit_days_comparison(project)
    response = HttpResponse(content_type="text/csv")
    result.to_csv(response)
    return response

def project_deficit_stats_csv(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    result = __get_deficit_stats_comparison(project)
    response = HttpResponse(content_type="text/csv")
    result.to_csv(response)
    return response

def project_deficit_days_plot(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    data = __get_deficit_days_comparison(project)
    plt.style.use('ggplot')
    fig, ax = __new_figure()
    data.plot(kind='bar', ax=ax, table=False)
    ax.set_title("Deficit days comparison")
    return __plot_to_response(fig)

def project_deficit_stats_plot(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    data = __get_deficit_stats_comparison(project)
    plt.style.use('ggplot')
    fig, ax = __new_figure()
    data.plot(kind='bar', ax=ax, table=False)
    ax.set_title("Median gap comparison")
    return __plot_to_response(fig)

def scenario(request, scenario_id):
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    context = {
        'scenario': scenario,
        'attribute_name': scenario.get_attribute_name(),
        'gap_attribute_name': scenario.get_gap_attribute_name(),
        'gage_type': Scenario.SOURCE_GAGE,
        'xslx_type': Scenario.SOURCE_EXCEL,
    }
    return render(request, 'flowviz/scenario.django.html', context)

def scenario_data(request, scenario_id):
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    data = scenario.get_data().to_json()
    return HttpResponse(data, content_type="application/json")

def dynamic_raster(request, scenario_id, attribute):
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    data = scenario.get_data()

    # Get visualization parameters
    cmap = request.GET.get('cmap', None)
    title = request.GET.get('title', None)
    zero = request.GET.get('zero', 'False')
    logscale = request.GET.get('logscale', 'False')

    zero = zero == "True"
    logscale = logscale == "True"

    plt.style.use('ggplot')
    fig = Figure()
    ax = fig.add_subplot(111)

    if not zero:
        min_value = data[attribute].min()
        max_value = data[attribute].max()
    else:
        min_value = data[attribute].min()
        max_value = abs(data[attribute].min())
    if cmap:
        colormap = cm.get_cmap(cmap)
        if zero:
            colormap = plotting.create_colormap(data, attribute, colormap, vmin=min_value, vmax=max_value)
        colormap.set_bad('black')
    else:
        colormap = None
    if logscale:
        if min_value <= 0:
            min_value = 0.001
        norm = matplotlib.colors.LogNorm(vmin=min_value, vmax=max_value)
    else:
        norm = None

    plotting.rasterplot(data, attribute, title, show_colorbar=True, norm=norm,
                           colormap=colormap, vmin=min_value, vmax=max_value, fig=fig, ax=ax)
    return __plot_to_response(fig)

def __new_figure():
    fig = Figure()
    ax = fig.add_subplot(111)
    return (fig, ax)

def __plot_to_response(fig):
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

def deficit_stats_plot(request, scenario_id):
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    data = scenario.get_data()
    plt.style.use('ggplot')
    fig, ax = __new_figure()
    title = "Gap (cfs/day)"
    plotting.deficit_stats_plot(data, scenario.get_gap_attribute_name(), title, fig, ax)
    return __plot_to_response(fig)

def deficit_days_plot(request, scenario_id):
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    data = scenario.get_data()
    plt.style.use('ggplot')
    fig, ax = __new_figure()
    title = "Percent of days in deficit"
    ax = plotting.deficit_days_plot(data, scenario.get_gap_attribute_name(), title, fig, ax)
    return __plot_to_response(fig)

def right_plot(request, scenario_id):
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    data = scenario.get_data()

    averages = data.groupby('dayofyear').mean()
    plt.style.use('ggplot')
    fig, ax = __new_figure()
    plotdata = averages[[
        scenario.get_attribute_name(),
        scenario.get_target_attribute_name()
    ]]
    plotdata.columns = [
        'Actual value',
        'Target value'
    ]
    plotdata.plot(ax=ax)
    ax.set_xlabel("Month")
    plotting.label_months(ax)
    return __plot_to_response(fig)
