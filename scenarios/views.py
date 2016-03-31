from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.core import serializers
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from waterkit.flow import plotting, analysis

from utils.mpl import new_figure, plot_to_response, to_percent

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

from models import Scenario, CyclicTargetElement
from forms import ScenarioForm, ScenarioGageForm, ScenarioExcelForm
from forms import CyclicTargetForm, CyclicTargetElementFormSet
from forms import FormGroup

DEFAULT_PLOT_STYLE = 'ggplot'

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
    return plot_to_response(fig)

def __label_scenario_attribute(scenario):
    return "Flow (cfs)"

def __label_volume_attribute(scenario):
    return "Volume (af)"

def __setup_scenario_plot(scenario_id):
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    plt.style.use(DEFAULT_PLOT_STYLE)
    return scenario, new_figure()

def deficit_stats_plot(request, scenario_id):
    scenario, (fig, ax) = __setup_scenario_plot(scenario_id)
    ax.set_ylabel(__label_volume_attribute(scenario))
    title = "Monthly Volume Deficit"
    plotting.volume_deficit_monthly(scenario.get_data(), scenario.get_gap_attribute_name(), title, fig, ax)
    return plot_to_response(fig)

def deficit_stats_plot_annual(request, scenario_id):
    scenario, (fig, ax) = __setup_scenario_plot(scenario_id)
    ax.set_ylabel(__label_volume_attribute(scenario))
    title = "Annual Volume Deficit"
    plotting.volume_deficit_annual(scenario.get_data(), scenario.get_gap_attribute_name(), title, fig, ax)
    return plot_to_response(fig)

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
    return plot_to_response(fig)

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
    return plot_to_response(fig)

def deficit_days_plot(request, scenario_id):
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    data = scenario.get_data()
    plt.style.use(DEFAULT_PLOT_STYLE)
    fig, ax = new_figure()
    title = "Monthly Temporal Deficit"
    ax = plotting.deficit_days_plot(data, scenario.get_gap_attribute_name(), title, fig, ax)
    ax.yaxis.set_major_formatter(FuncFormatter(to_percent))
    ax.set_ylim([0.0, 1.0])
    return plot_to_response(fig)

def annual_deficit_days_plot(request, scenario_id):
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    data = scenario.get_data()
    plt.style.use(DEFAULT_PLOT_STYLE)
    fig, ax = new_figure()
    title = "Annual Temporal Deficit"
    ax = plotting.annual_deficit_days_plot(
        data,
        scenario.get_gap_attribute_name(),
        title, fig, ax
    )
    ax.yaxis.set_major_formatter(FuncFormatter(to_percent))
    ax.set_ylim([0.0, 1.0])
    return plot_to_response(fig)

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
    fig, ax = new_figure()
    plotdata.plot(ax=ax)
    ax.set_xlabel("Month")
    ax.set_ylabel(__label_scenario_attribute(scenario))
    plotting.label_months(ax)
    return plot_to_response(fig)

def long_term_minimum_plot(request, scenario_id):
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    data = scenario.get_data()

    column = scenario.get_attribute_name()
    min_data = analysis.annual_minimum(data[column], 7, True)
    plt.style.use(DEFAULT_PLOT_STYLE)
    fig, ax = new_figure()
    plotting.plot_with_trendline_ols(
        min_data,
        title="7-day Minimum Flow",
        fig=fig, ax=ax)
    ax.set_xlabel("Year")
    ax.set_ylabel(__label_scenario_attribute(scenario))
    return plot_to_response(fig)

@login_required
def scenario_edit(request, scenario_id):
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    if request.method == "POST":
        form_group = FormGroup(
            common_form = ScenarioForm(request.POST, instance=scenario),
            gage_form = ScenarioGageForm(request.POST, instance=scenario),
            excel_form = ScenarioExcelForm(request.POST, instance=scenario),
            cyclic_target_form = CyclicTargetForm(request.POST, instance=scenario.target),
            cyclic_target_element_formset = CyclicTargetElementFormSet(request.POST, instance=scenario.target),
        )
        if form_group.is_valid():
            form_group.save()
            return redirect("scenario", scenario_id=scenario.id)
    else:
        form_group = FormGroup(
            common_form = ScenarioForm(instance=scenario),
            gage_form = ScenarioGageForm(instance=scenario),
            excel_form = ScenarioExcelForm(instance=scenario),
            cyclic_target_form = CyclicTargetForm(instance=scenario.target),
            cyclic_target_element_formset = CyclicTargetElementFormSet(instance=scenario.target),
        )

    context = {
        "title": "Edit Scenario",
        "year": datetime.now().year,
        "scenario_id": scenario.id,
        "common_form": form_group.common_form,
        "gage_form": form_group.gage_form,
        "excel_form": form_group.excel_form,
        "cyclic_target_form": form_group.cyclic_target_form,
        "cyclic_target_element_formset": form_group.cyclic_target_element_formset,
    }
    return render(request, "scenarios/scenario_edit.django.html", context)
