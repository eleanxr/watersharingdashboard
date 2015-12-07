from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseBadRequest
from django.core import serializers

from models import Project, Scenario, CyclicTargetElement

from waterkit import plotting, analysis
from waterkit.analysis import CFS_TO_AFD

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from pylab import figure
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.colors
from matplotlib.ticker import FuncFormatter

from datetime import datetime

import pandas as pd

import json

DEFAULT_PLOT_STYLE = 'ggplot'

import logging
logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'flowviz/index.django.html')

def projects(request):
    projects = Project.objects.all().order_by('name')
    return render(request, 'flowviz/projects.django.html',{
        'projects': projects,
        'title': 'Projects',
        'year': datetime.now().year,
    })

def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    huc_scale = project.huc_scale
    if not huc_scale:
        huc_scale = ""
    huc_regions = map(lambda r: r.hucid, project.hucregion_set.all())

    usgs_ids = []
    for s in project.scenario_set.all():
        if s.gage_location:
            usgs_ids.append(s.gage_location.identifier)

    context = {
        'project': project,
        'title': project.name,
        'year': datetime.now().year,
        'huc_scale': huc_scale,
        'huc_regions': json.dumps(huc_regions),
        'usgs_gages': json.dumps(usgs_ids)
    }
    return render(request, 'flowviz/project.django.html', context)

def project_compare(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    context = {
        'project': project,
    }
    return render(request, 'flowviz/project_compare.django.html', context)

def __get_deficit_days_comparison(project, analysis_f, index_name):
    """
    Get the temporal deficit comparison for a project.

    analysis_f : f(data, gap_attribute_name, target_attribute_name)
        The function that returns the annual temporal information.
    index_name : string
        The name to use for the resulting DataFrame's index.
    """
    datasets = []
    names = []
    for scenario in project.scenario_set.all():
    	try:
    	    data = scenario.get_data()
    	    attribute_name = scenario.get_gap_attribute_name()
    	    target_attribute_name = scenario.get_target_attribute_name()
    	    data_pct = analysis_f(data, attribute_name, target_attribute_name)
    	    data_pct.index.name = index_name
    	    datasets.append(data_pct)
    	    names.append(scenario.name)
        except:
            pass
    return analysis.compare_series(datasets, names)

def __get_deficit_stats_comparison(project, analysis_f, units):
    """
    The  the deficit stats comparison dataset for a project.

    Parameters
    ==========
    analysis_f : f(data, gap_attribute_name, target_attribute_name)
        The function that returns the monthly stats dataset for a scenario
    """
    datasets = []
    names = []
    for scenario in project.scenario_set.all():
        try:
            data = scenario.get_data()
            attribute_name = scenario.get_gap_attribute_name()
            target_name = scenario.get_target_attribute_name()
            monthly_values = analysis_f(data, attribute_name, target_name)
            monthly_values.index.name = "Month"
            monthly_values.name = attribute_name
            datasets.append(monthly_values)
            names.append(scenario.name + " (%s)" % units)
        except:
            pass
    return analysis.compare_series(datasets, names)

def project_data(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    result = __get_deficit_days_comparison(
        project,
        lambda d, g, t: analysis.monthly_deficit_pct(d, g),
        "Month")
    response = HttpResponse(content_type="application/json")
    result.to_json(response, orient='index')
    return response

#
# Deficit days percent methods. Refactor to API.
#

def project_deficit_days_csv(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    result = __get_deficit_days_comparison(project,
        lambda d, g, t: analysis.monthly_deficit_pct(d, g),
        "Month")
    response = HttpResponse(content_type="text/csv")
    result.to_csv(response)
    return response

def project_deficit_days_annual_csv(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    result = __get_deficit_days_comparison(project,
        lambda d, g, t: analysis.annual_deficit_pct(d, g), "Annual Average").mean()
    response = HttpResponse(content_type="text/csv")
    result.to_csv(response, index_label="Scenario", header=['Annual Average'])
    return response

def project_deficit_days_plot(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    data = __get_deficit_days_comparison(
        project,
        lambda d, g, t: analysis.monthly_deficit_pct(d, g),
        "Month"
    )
    plt.style.use(DEFAULT_PLOT_STYLE)
    fig, ax = __new_figure()
    data.plot(kind='bar', ax=ax, table=False)
    ax.set_title("Deficit days comparison")
    ax.yaxis.set_major_formatter(FuncFormatter(to_percent))
    ax.set_ylim([0.0, 1.0])
    return __plot_to_response(fig)

#
# Deficit stats volume/percent methods. Refactor to API.
#

def __dataframe_csv_helper(request, project_id, analysis_f, units):
    project = get_object_or_404(Project, pk=project_id)
    result = __get_deficit_stats_comparison(project, analysis_f, units)
    response = HttpResponse(content_type="text/csv")
    result.to_csv(response)
    return response

def __dataframe_annual_csv_helper(request, project_id, analysis_f, units):
    project = get_object_or_404(Project, pk=project_id)
    # This line is the only difference from the above function. There has to
    # be a better way of unifying these!
    result = __get_deficit_stats_comparison(project, analysis_f, units).mean().abs()
    response = HttpResponse(content_type="text/csv")
    # Take the transpose of the series to get a row vector instead of a column
    # vector.
    transpose = result.to_frame().transpose()
    transpose.to_csv(response, index=False)
    return response

def __dataframe_barplot_helper(request, project_id, title, analysis_f,
    units=None, formatter=None, xlim=None, ylim=None):
    project = get_object_or_404(Project, pk=project_id)
    data = __get_deficit_stats_comparison(project, analysis_f, units)
    plt.style.use(DEFAULT_PLOT_STYLE)
    fig, ax = __new_figure()
    data.plot(kind='bar', ax=ax, table=False)
    ax.set_title(title)
    if formatter:
        ax.yaxis.set_major_formatter(formatter)
    ylabel = "Volume"
    ax.set_ylabel("Volume (%s)" % units)

    if xlim:
        ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)

    return __plot_to_response(fig)

def project_deficit_stats_pct_csv(request, project_id):
    return __dataframe_csv_helper(request, project_id,
        lambda d, g, t: analysis.monthly_volume_deficit_pct(d, g, t, CFS_TO_AFD).mean().abs(),
        "%")

def project_deficit_stats_annual_pct_csv(request, project_id):
    """
    Stream a CSV with the annual volume deficit stats.
    """
    return __dataframe_annual_csv_helper(request, project_id,
        lambda d, g, t: analysis.annual_volume_deficit_pct(d, g, t, CFS_TO_AFD), "%")

def project_deficit_stats_csv(request, project_id):
    return __dataframe_csv_helper(request, project_id,
        lambda d, g, t: analysis.monthly_volume_deficit(d, g, CFS_TO_AFD).mean().abs(),
        "af")

def project_deficit_stats_annual_csv(request, project_id):
    return __dataframe_annual_csv_helper(request, project_id,
        lambda d, g, t: analysis.annual_volume_deficit(d, g, CFS_TO_AFD), "af")

def project_deficit_stats_plot(request, project_id):
    return __dataframe_barplot_helper(request, project_id, "Average monthly volume deficit",
        lambda d, g, t: analysis.monthly_volume_deficit(d, g, CFS_TO_AFD).mean().abs(),
        "af")

def project_deficit_stats_pct_plot(request, project_id):
    return __dataframe_barplot_helper(request, project_id,
        "Average monthly volume deficit relative to target",
        lambda d, g, t: analysis.monthly_volume_deficit_pct(d, g, t, CFS_TO_AFD).mean().abs(),
        "%", formatter=FuncFormatter(to_percent), ylim=[0.0, 1.0])

def get_low_flows(project_id):
    project = get_object_or_404(Project, pk=project_id)
    names = []
    values = []
    for scenario in project.scenario_set.all():
        try:
            data = scenario.get_data()
            value = analysis.low_flow_trend_pct(data[scenario.get_attribute_name()], 7, False)
            values.append(value)
            names.append(scenario.name)
        except:
            pass
    frame = pd.Series(values, index=names)
    frame.name = "Trend"
    frame.index.name = "Scenario"

    return frame

def project_low_flow_csv(request, project_id):
    frame = get_low_flows(project_id)
    response = HttpResponse(content_type='text/csv')
    frame.to_csv(response, index=True, header=True)
    return response

def project_low_flow_plot(request, project_id):
    low_flows = get_low_flows(project_id)
    plt.style.use(DEFAULT_PLOT_STYLE)
    fig, ax = __new_figure()
    low_flows.plot(kind='bar', fig=fig, ax=ax)
    ax.yaxis.set_major_formatter(FuncFormatter(to_percent))
    ax.set_title("7-day Minimum Flow Trend")
    labels = ax.get_xticklabels()
    for label in labels:
        label.set_rotation(0)
    return __plot_to_response(fig)

#
# Scenario methods.
#

def scenario(request, scenario_id):
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    def convert_element(element):
        return CyclicTargetElement(
            target_value = float(element.target_value) * scenario.attribute_multiplier,
            from_month = element.from_month,
            from_day = element.from_day,
            to_month = element.to_month,
            to_day = element.to_day
        )
    if scenario.source_type == Scenario.SOURCE_GAGE:
        converted_targets = map(convert_element,
            scenario.target.cyclictargetelement_set.all())
    else:
        converted_targets = None
    context = {
        'scenario': scenario,
        'attribute_name': scenario.get_attribute_name(),
        'gap_attribute_name': scenario.get_gap_attribute_name(),
        'converted_targets': converted_targets,
        'gage_type': Scenario.SOURCE_GAGE,
        'xslx_type': Scenario.SOURCE_EXCEL,
        'title': scenario.name,
        'year': datetime.now().year,
    }
    return render(request, 'flowviz/scenario.django.html', context)

def scenario_data(request, scenario_id):
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    data = scenario.get_data().to_json()
    return HttpResponse(data, content_type="application/json")

def dynamic_raster(request, scenario_id):
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    data = scenario.get_data()

    # Get visualization parameters
    attribute = request.GET.get('attribute', None)
    if not attribute:
        return HttpResponseBadRequest()
    cmap = request.GET.get('cmap', None)
    title = request.GET.get('title', None)
    zero = request.GET.get('zero', 'False')
    logscale = request.GET.get('logscale', 'False')

    zero = zero == "True"
    logscale = logscale == "True"

    plt.style.use(DEFAULT_PLOT_STYLE)
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

def __label_scenario_attribute(scenario):
    return "Flow (cfs)"

def __label_volume_attribute(scenario):
    return "Volume (af)"

def __setup_scenario_plot(scenario_id):
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    plt.style.use(DEFAULT_PLOT_STYLE)
    return scenario, __new_figure()

def to_percent(y, position):
    s = str(100 * y)
    # The percent symbol needs escaping in latex
    if matplotlib.rcParams['text.usetex'] == True:
        return s + r'$\%$'
    else:
        return s + '%'

def deficit_stats_plot(request, scenario_id):
    scenario, (fig, ax) = __setup_scenario_plot(scenario_id)
    ax.set_ylabel(__label_volume_attribute(scenario))
    title = "Monthly Volume Deficit"
    plotting.volume_deficit_monthly(scenario.get_data(), scenario.get_gap_attribute_name(), title, fig, ax)
    return __plot_to_response(fig)

def deficit_stats_plot_annual(request, scenario_id):
    scenario, (fig, ax) = __setup_scenario_plot(scenario_id)
    ax.set_ylabel(__label_volume_attribute(scenario))
    title = "Annual Volume Deficit"
    plotting.volume_deficit_annual(scenario.get_data(), scenario.get_gap_attribute_name(), title, fig, ax)
    return __plot_to_response(fig)

def deficit_stats_pct_plot(request, scenario_id):
    scenario, (fig, ax) = __setup_scenario_plot(scenario_id)
    ax.yaxis.set_major_formatter(FuncFormatter(to_percent))
    ax.set_ylim([0.0, 1.0])
    plotting.volume_deficit_pct_monthly(
        scenario.get_data(),
        scenario.get_gap_attribute_name(),
        scenario.get_target_attribute_name(),
        "Monthly Volume Deficit Relative to Target",
        fig, ax
    )
    return __plot_to_response(fig)

def deficit_stats_pct_plot_annual(request, scenario_id):
    scenario, (fig, ax) = __setup_scenario_plot(scenario_id)
    ax.yaxis.set_major_formatter(FuncFormatter(to_percent))
    ax.set_ylim([0.0, 1.0])
    plotting.volume_deficit_pct_annual(
        scenario.get_data(),
        scenario.get_gap_attribute_name(),
        scenario.get_target_attribute_name(),
        "Annual Volume Deficit Relative to Target",
        fig, ax
    )
    return __plot_to_response(fig)

def deficit_days_plot(request, scenario_id):
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    data = scenario.get_data()
    plt.style.use(DEFAULT_PLOT_STYLE)
    fig, ax = __new_figure()
    title = "Monthly Temporal Deficit"
    ax = plotting.deficit_days_plot(data, scenario.get_gap_attribute_name(), title, fig, ax)
    ax.yaxis.set_major_formatter(FuncFormatter(to_percent))
    ax.set_ylim([0.0, 1.0])
    return __plot_to_response(fig)

def annual_deficit_days_plot(request, scenario_id):
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    data = scenario.get_data()
    plt.style.use(DEFAULT_PLOT_STYLE)
    fig, ax = __new_figure()
    title = "Annual Temporal Deficit"
    ax = plotting.annual_deficit_days_plot(
        data,
        scenario.get_gap_attribute_name(),
        title, fig, ax
    )
    ax.yaxis.set_major_formatter(FuncFormatter(to_percent))
    ax.set_ylim([0.0, 1.0])
    return __plot_to_response(fig)

def right_plot(request, scenario_id):
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    data = scenario.get_data()

    daygroups = data.groupby('dayofyear')
    low = daygroups[scenario.get_attribute_name()].quantile(0.2)
    median = daygroups[scenario.get_attribute_name()].quantile(0.5)
    high = daygroups[scenario.get_attribute_name()].quantile(0.8)
    target = daygroups[scenario.get_target_attribute_name()].mean()

    plotdata = pd.concat([low, median, high, target], axis=1)
    plotdata.columns = ["80% Exceedance", "Median", "20% Exceedance", "Target"]

    plt.style.use(DEFAULT_PLOT_STYLE)
    fig, ax = __new_figure()
    plotdata.plot(ax=ax)
    ax.set_xlabel("Month")
    ax.set_ylabel(__label_scenario_attribute(scenario))
    plotting.label_months(ax)
    return __plot_to_response(fig)

def long_term_minimum_plot(request, scenario_id):
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    data = scenario.get_data()

    column = scenario.get_attribute_name()
    min_data = analysis.annual_minimum(data[column], 7, True)
    plt.style.use(DEFAULT_PLOT_STYLE)
    fig, ax = __new_figure()
    plotting.plot_with_trendline_ols(
        min_data,
        title="7-day Minimum Flow",
        fig=fig, ax=ax)
    ax.set_xlabel("Year")
    ax.set_ylabel(__label_scenario_attribute(scenario))
    return __plot_to_response(fig)
