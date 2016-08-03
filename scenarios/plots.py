import pandas as pd

from waterkit.climate import analysis, plotting
import waterkit.flow.analysis as flow_analysis

from bokeh.models import Range1d, NumeralTickFormatter, YearsTicker, SingleIntervalTicker

import utils.bokeh

from utils.mpl import new_figure, plot_to_response, to_percent

def plot_drought_deficit(scenario, annual_data, quantile):
    flowdata = scenario.get_data()
    if scenario.critical_season_begin and scenario.critical_season_end:
        season = (
            scenario.critical_season_begin,
            scenario.critical_season_end
        )
    else:
        season = None
    drought_analysis = analysis.DroughtYearFromFlowAnalysis(
        flowdata[scenario.get_attribute_name()],
        quantile,
        season = season
    )
    gap_attribute = scenario.get_gap_attribute_name()
    year_range = Range1d(annual_data.index.min(), annual_data.index.max())
    plot_builder = plotting.DroughtPlotBuilder(
        drought_analysis,
        annual_data,
        tools=utils.bokeh.DEFAULT_TOOLS,
        logo=None,
        continuous_range=year_range,
        responsive=True,
    )
    plot = plot_builder.plot()
    return plot

def plot_drought_deficit_mpl(scenario, annual_data, quantile):
    flowdata = scenario.get_data()
    if scenario.critical_season_begin and scenario.critical_season_end:
        season = (
            scenario.critical_season_begin,
            scenario.critical_season_end
        )
    else:
        season = None
    drought_analysis = analysis.DroughtYearFromFlowAnalysis(
        flowdata[scenario.get_attribute_name()],
        quantile,
        season = season
    )
    data = annual_data.to_frame(name='Annual').merge(
        drought_analysis.label_years().to_frame("In Drought"),
        how='left',
        left_index=True,
        right_index=True
    ).dropna()
    fig, ax = new_figure()
    data['Annual'].plot(
        kind='bar',
        ax=ax,
        color=data['In Drought'].map({True: 'r', False: 'g'})
    )
    return fig, ax

def plot_drought_temporal_deficit_mpl(scenario, quantile=0.1):
    flowdata = scenario.get_data()
    gap_attribute = scenario.get_gap_attribute_name()
    temporal_deficit = flow_analysis.annual_deficit_pct(flowdata[gap_attribute])
    return plot_drought_deficit_mpl(scenario, temporal_deficit, quantile)

def plot_drought_volume_deficit_mpl(scenario, quantile=0.1):
    flowdata = scenario.get_data()
    gap_attribute = scenario.get_gap_attribute_name()
    volume_deficit = flow_analysis.annual_volume_deficit(
        flowdata, gap_attribute
    ).abs()
    return plot_drought_deficit_mpl(scenario, volume_deficit, quantile)

def plot_drought_temporal_deficit(scenario, quantile=0.1):
    flowdata = scenario.get_data()
    gap_attribute = scenario.get_gap_attribute_name()
    temporal_deficit = flow_analysis.annual_deficit_pct(flowdata[gap_attribute])
    plot = plot_drought_deficit(scenario, temporal_deficit, quantile)
    plot.y_range = Range1d(0, 1)
    plot._yaxis.formatter = NumeralTickFormatter(format="00%")
    plot.title = "Temporal deficit during drought"
    plot._yaxis.axis_label = "Temporal Deficit (% days)"
    return plot

def plot_drought_volume_deficit(scenario, quantile=0.1):
    volume_deficit = flow_analysis.annual_volume_deficit(
        scenario.get_data(), scenario.get_gap_attribute_name()).abs()
    plot = plot_drought_deficit(scenario, volume_deficit, quantile)
    plot._yaxis.formatter = NumeralTickFormatter(format="0,0")
    plot._yaxis.axis_label = "Deficit (AF)"
    plot.title = "Volume deficit during drought"
    return plot
