from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.defaultfilters import slugify

from models import CropMix, ApiKey

from bokeh.charts import Area, Bar
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.models import Range1d, NumeralTickFormatter, CategoricalTickFormatter
from bokeh.palettes import Spectral9

import pandas as pd

from waterkit import econ, usda_data

from datetime import datetime
import tempfile, shutil

DEFAULT_TOOLS = "pan,box_zoom,resize,reset,save"
EXCEL_CONTENT_TYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

def create_nass_client():
    keys = ApiKey.objects.filter(use_key = True, system = "USDA NASS")
    if not keys:
        raise Exception("No USDA NASS API keys have been configured.")
    return usda_data.NASSDataSource(keys[0].key)

def get_bls_key():
    keys = ApiKey.objects.filter(use_key=True, system="BLS")
    if not keys:
        raise Exception("No BLS API keys have been configured.")
    return keys[0].key

def read_crop_mix(crop_mix_id):
    """Read the crop mix data given its id. Returns a tuple with
    (crop_mix, data, years, commodities).
    """
    crop_mix = get_object_or_404(CropMix, pk=crop_mix_id)

    years = map(lambda y: y.year, crop_mix.cropmixyear_set.all())
    commodities = map(lambda c: c.commodity, crop_mix.cropmixcommodity_set.all())

    connection = create_nass_client()
    data = econ.NASSCropMixDataSet(
        connection,
        crop_mix.state,
        crop_mix.county,
        years,
        commodities
    )
    return crop_mix, data, years, commodities

def crop_mix_detail(request, crop_mix_id):
    crop_mix, data, years, commodities = read_crop_mix(crop_mix_id)
    bls_key = get_bls_key()

    # We take the top 8 columns of all tables below because we're going to use
    # a 9 color palette to display the data.

    acreage_table = econ.select_top_n_columns(data.get_table('ACRES'), 8)
    acre_plot = Area(
        acreage_table.reset_index(),
        x='year',
        y=map(str, acreage_table.columns),
        stack=True,
        legend='bottom_right',
        xlabel="Year",
        ylabel="Acres",
        title="# Acres by crop type",
        palette=Spectral9,
        tools=DEFAULT_TOOLS,
        logo=None,
        responsive=True
    )
    acre_plot.x_range = Range1d(acreage_table.index.min(), acreage_table.index.max())
    acre_plot.y_range = Range1d(0, acreage_table.max().sum())
    acre_plot._xaxis.formatter = CategoricalTickFormatter()
    acre_plot._yaxis.formatter = NumeralTickFormatter(format='0,0')
    acre_script, acre_div = components(acre_plot, CDN)

    acreage_pct_table = econ.select_top_n_columns(data.get_ratio_table('ACRES'), 8)
    acreage_pct_stacked = acreage_pct_table.stack().reset_index()
    acreage_pct_stacked.columns = ['year', 'commodity_desc', 'value']
    acre_pct_plot = Bar(
        acreage_pct_stacked,
        label = 'year',
        stack= 'commodity_desc',
        values='value',
        xlabel='Year',
        ylabel='',
        title='% Acres by crop type',
        palette=Spectral9,
        legend='bottom_right',
        tools=DEFAULT_TOOLS,
        logo=None,
        responsive=True
    )
    acre_pct_plot.y_range = Range1d(0, 1)
    acre_pct_plot._yaxis.formatter = NumeralTickFormatter(format='0%')
    acre_pct_script, acre_pct_div = components(acre_pct_plot, CDN)

    revenue_table = econ.select_top_n_columns(data.get_table('$'), 8)
    revenue_table = econ.adjust_cpi(revenue_table, bls_key, crop_mix.cpi_adjustment_year)
    revenue_stacked = revenue_table.stack().reset_index()
    revenue_stacked.columns = ['year', 'commodity_desc', 'value']
    revenue_plot = Bar(
        revenue_stacked,
        label='year',
        title='Gross Revenue (%d $)' % crop_mix.cpi_adjustment_year,
        stack='commodity_desc',
        values='value',
        palette=Spectral9,
        legend='bottom_right',
        xlabel='Year',
        ylabel='',
        tools=DEFAULT_TOOLS,
        logo=None,
        responsive=True
    )
    revenue_plot._yaxis.formatter = NumeralTickFormatter(format='$0,0')
    revenue_script, revenue_div = components(revenue_plot, CDN)

    context = {
        'id': crop_mix_id,
        'title': crop_mix.name,
        'description': crop_mix.description,
        'state': crop_mix.state,
        'county': crop_mix.county,
        'years': ', '.join(map(str, years)),
        'commodities': ', '.join(commodities),
        'acre_script': acre_script,
        'acre_div': acre_div,
        'acre_pct_script': acre_pct_script,
        'acre_pct_div': acre_pct_div,
        'year': datetime.now().year,
        'source': crop_mix.source,
        'revenue_script': revenue_script,
        'revenue_div': revenue_div,
    }

    return render(request, 'econ/crop_mix_detail.django.html', context)

def download_crop_mix_area_data(request, crop_mix_id):
    crop_mix, data, years, commodities = read_crop_mix(crop_mix_id)
    with tempfile.NamedTemporaryFile(suffix='.xlsx') as excelfile:
        writer = pd.ExcelWriter(excelfile.name)
        data.data.to_excel(writer)
        writer.save()
        response = HttpResponse(content_type=EXCEL_CONTENT_TYPE)
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % slugify(crop_mix.name)
        shutil.copyfileobj(excelfile, response)
        return response
