from bokeh.models import NumeralTickFormatter, CategoricalTickFormatter, Range1d
from bokeh.palettes import Spectral9
from bokeh.resources import CDN
from bokeh.embed import components

from waterkit.econ import analysis, plotting, usda_data

import utils.bokeh

DEFAULT_TOOLS = utils.bokeh.DEFAULT_TOOLS

def plot_labor_table(labor_table):
    return plotting.bar_plot_table(
        labor_table.div(2080),
        title='Labor (FTEs 2,080 hours/year)',
        palette=Spectral9,
        legend='bottom_right',
        xlabel='Year',
        ylabel='FTEs 2,080 hours/year',
        tools=DEFAULT_TOOLS,
        logo=None,
        responsive=True,
        number_of_categories=8,
        yaxis_formatter=NumeralTickFormatter(format='0,0')
    )

def plot_revenue_af_table(revenue_table, niwr_table):
    revenue_af_table = revenue_table.sum(axis=1) / niwr_table.sum(axis=1)
    return plotting.line_plot_series(
        revenue_af_table,
        title = "Revenue per Acre-Foot",
        xlabel = "Year",
        ylabel = "$/AF",
        responsive = True,
        yaxis_formatter = NumeralTickFormatter(format="$0,0"),
        y_range = Range1d(0.0, revenue_af_table.max() * 1.1),
        line_width = 4,
        tools=DEFAULT_TOOLS,
        logo=None,
    )

def plot_acres(econ_data, groups):
    return plotting.area_plot_table(
        econ_data.get_table('ACRES', groups),
        legend='bottom_right',
        xlabel="Year",
        ylabel="Acres",
        title="# Acres by crop type",
        palette=Spectral9,
        tools=DEFAULT_TOOLS,
        logo=None,
        responsive=True,
        number_of_categories=8,
        yaxis_formatter=NumeralTickFormatter(format="0,0")
    )

def plot_acre_fractions(econ_data, groups):
    return plotting.bar_plot_table(
        econ_data.get_ratio_table('ACRES', groups),
        xlabel='Year',
        ylabel='',
        title='% Acres by crop type',
        palette=Spectral9,
        legend='bottom_right',
        tools=DEFAULT_TOOLS,
        logo=None,
        responsive=True,
        number_of_categories=8,
        yaxis_formatter=NumeralTickFormatter(format='00%'),
        y_range=Range1d(0.0, 1.0)
    )
