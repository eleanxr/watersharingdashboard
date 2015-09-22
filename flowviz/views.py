from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.core import serializers

from models import Project, Scenario, CyclicTargetElement
import units

from waterkit import plotting, analysis

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from pylab import figure
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.colors
from matplotlib.ticker import FuncFormatter

import pandas as pd

DEFAULT_PLOT_STYLE = 'ggplot'

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
        data_pct = analysis.monthly_deficit_pct(data, attribute_name)
        data_pct.index.name = "Month"
        names.append(scenario.name)
        datasets.append(data_pct)
    return analysis.compare_datasets(datasets, 'pct', names)

def __get_deficit_stats_comparison(project, analysis_f):
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
        data = scenario.get_data()
        attribute_name = scenario.get_gap_attribute_name()
        target_name = scenario.get_target_attribute_name()
        unit_abbr = units.get_volume_unit(scenario.attribute_units_abbr)
        names.append(scenario.name + " (" + unit_abbr + ")")
        monthly_values = analysis_f(data, attribute_name, target_name)
        averages = monthly_values.mean().abs()
        averages.index.name = "Month"
        averages.name = attribute_name
        datasets.append(monthly_values.mean().abs())
    return analysis.compare_series(datasets, names)

def project_data(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    result = __get_deficit_days_comparison(project)
    response = HttpResponse(content_type="application/json")
    result.to_json(response, orient='index')
    return response

#
# Deficit days percent methods. Refactor to API.
#

def project_deficit_days_csv(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    result = __get_deficit_days_comparison(project)
    response = HttpResponse(content_type="text/csv")
    result.to_csv(response)
    return response

def project_deficit_days_plot(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    data = __get_deficit_days_comparison(project)
    plt.style.use(DEFAULT_PLOT_STYLE)
    fig, ax = __new_figure()
    data.plot(kind='bar', ax=ax, table=False)
    ax.set_title("Deficit days comparison")
    ax.yaxis.set_major_formatter(FuncFormatter(to_percent))
    return __plot_to_response(fig)

#
# Deficit stats volume/percent methods. Refactor to API.
#

def __dataframe_csv_helper(request, project_id, analysis_f):
    project = get_object_or_404(Project, pk=project_id)
    result = __get_deficit_stats_comparison(project, analysis_f)
    response = HttpResponse(content_type="text/csv")
    result.to_csv(response)
    return response

def __dataframe_barplot_helper(request, project_id, title, analysis_f,
    formatter=None):
    project = get_object_or_404(Project, pk=project_id)
    data = __get_deficit_stats_comparison(project, analysis_f)
    plt.style.use(DEFAULT_PLOT_STYLE)
    fig, ax = __new_figure()
    data.plot(kind='bar', ax=ax, table=False)
    ax.set_title(title)
    if formatter:
        ax.yaxis.set_major_formatter(formatter)
    name_set = set(map(lambda s: s.attribute_name, project.scenario_set.all()))
    units_set = set(map(lambda s: units.get_volume_unit(s.attribute_units_abbr), project.scenario_set.all()))
    if len(name_set) == 1 and len(units_set) == 1:
        ax.set_ylabel("%s Deficit (%s)" % (name_set.pop(), units_set.pop()))
    return __plot_to_response(fig)

def project_deficit_stats_pct_csv(request, project_id):
    return __dataframe_csv_helper(request, project_id,
        lambda data, gap, target: analysis.monthly_volume_deficit_pct(data, gap, target))

def project_deficit_stats_csv(request, project_id):
    return __dataframe_csv_helper(request, project_id,
        lambda data, gap, target: analysis.monthly_volume_deficit(data, gap))

def project_deficit_stats_plot(request, project_id):
    return __dataframe_barplot_helper(request, project_id, "Monthly volume deficit",
        lambda d, g, t: analysis.monthly_volume_deficit(d, g))

def project_deficit_stats_pct_plot(request, project_id):
    return __dataframe_barplot_helper(request, project_id,
        "Monthly volume deficit relative to target",
        lambda d, g, t: analysis.monthly_volume_deficit_pct(d, g, t),
        formatter=FuncFormatter(to_percent))
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
    return "%s (%s)" % (scenario.attribute_name, scenario.attribute_units_abbr)

def __label_volume_attribute(scenario):
    volume_unit = units.get_volume_unit(scenario.attribute_units_abbr)
    if volume_unit:
        return "Volume (%s)" % volume_unit
    else:
        return "Volume"

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
    return __plot_to_response(fig)

def right_plot(request, scenario_id):
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    data = scenario.get_data()

    averages = data.groupby('dayofyear').mean()
    plt.style.use(DEFAULT_PLOT_STYLE)
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
    ax.set_ylabel(__label_scenario_attribute(scenario))
    plotting.label_months(ax)
    return __plot_to_response(fig)
