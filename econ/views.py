from django.shortcuts import render, get_object_or_404

from models import CropMix, NASSApiKey

from bokeh.charts import Area
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.models import Range1d

from waterkit import econ, usda_data

def create_nass_client():
    keys = NASSApiKey.objects.filter(use_key = True)
    if not keys:
        raise Exception("No USDA NASS API keys have been configured.")
    return usda_data.NASSDataSource(keys[0].key)

def crop_mix_detail(request, crop_mix_id):
    crop_mix = get_object_or_404(CropMix, pk=crop_mix_id)

    connection = create_nass_client()
    data = econ.read_nass_crop_mix(
        connection,
        crop_mix.state,
        crop_mix.county,
        'ACRES',
        map(lambda y: y.year, crop_mix.cropmixyear_set.all()),
        map(lambda c: c.commodity, crop_mix.cropmixcommodity_set.all())
    )

    acre_plot = Area(
        data.reset_index().fillna(0),
        x='year',
        y=map(str, data.columns),
        stack=True,
        legend='bottom_right',
        xlabel="Year",
        ylabel="Acres",
        title="# Acres by crop type")
    acre_plot.x_range = Range1d(data.index.min(), data.index.max())
    acre_plot.y_range = Range1d(0, data.max().sum())

    acre_script, acre_div = components(acre_plot, CDN)

    context = {
        'name': crop_mix.name,
        'acre_script': acre_script,
        'acre_div': acre_div
    }

    return render(request, 'econ/crop_mix_detail.django.html', context)
