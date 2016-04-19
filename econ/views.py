from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.defaultfilters import slugify
from django.views.generic import View
from django.forms import  inlineformset_factory

from models import CropMix, ApiKey, ConsumerPriceIndexData, CropMixGroup
import forms
import plots
import models

from datafiles.forms import FileUploadForm

from bokeh.models import NumeralTickFormatter, CategoricalTickFormatter, Range1d
from bokeh.palettes import Spectral9
from bokeh.resources import CDN
from bokeh.embed import components

import pandas as pd

from waterkit.econ import analysis, plotting, usda_data

from datetime import datetime
import tempfile, shutil
from functools import partial, wraps

from utils.views import EditObjectView
from utils.forms import bind_form_parameters

from plots import DEFAULT_TOOLS
EXCEL_CONTENT_TYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

def create_nass_client():
    return models.create_nass_client()

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

    data, years, commodities = crop_mix.get_data()
    return crop_mix, data, years, commodities

def crop_mix_detail(request, crop_mix_id):
    crop_mix, data, years, commodities = read_crop_mix(crop_mix_id)
    bls_key = get_bls_key()

    groups = map(lambda g: g.as_cropgroup(), crop_mix.cropmixgroup_set.all())

    context = {
        'id': crop_mix_id,
        'crop_mix': crop_mix,
        'title': crop_mix.name,
        'description': crop_mix.description,
        'state': crop_mix.state,
        'county': crop_mix.county,
        'years': ', '.join(map(str, years)),
        'commodities': ', '.join(commodities),
        'year': datetime.now().year,
        'source': crop_mix.source,
    }


    # We take the top 8 columns of all charts below because we're going to use
    # a 9 color palette to display the data.

    acre_plot = plotting.area_plot_table(
        data.get_table('ACRES', groups),
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
    acre_script, acre_div = components(acre_plot, CDN)
    context.update({
        'acre_script': acre_script,
        'acre_div': acre_div,
    })

    acre_pct_plot = plotting.bar_plot_table(
        data.get_ratio_table('ACRES', groups),
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
    acre_pct_script, acre_pct_div = components(acre_pct_plot, CDN)
    context.update({
        'acre_pct_script': acre_pct_script,
        'acre_pct_div': acre_pct_div,
    })

    if groups:
        group_map, uncategorized = data.get_group_map(groups)
        group_values = {g.title: g for g in groups}
        context.update({
            'group_map': {
                key: (group_values[key], ', '.join(value))
                for key, value in group_map.items()
            },
            'uncategorized': ", ".join(uncategorized),
        })
        revenue_table = data.get_derived_table("Revenue", groups)

        niwr_table = data.get_derived_table("NIWR", groups)
        niwr_plot = plotting.bar_plot_table(
            niwr_table,
            title='Water Use (acre-feet)',
            palette=Spectral9,
            legend='bottom_right',
            xlabel='Year',
            ylabel='Acre-Feet',
            tools=DEFAULT_TOOLS,
            logo=None,
            responsive=True,
            number_of_categories=8,
            yaxis_formatter=NumeralTickFormatter(format='0,0')
        )
        niwr_script, niwr_div = components(niwr_plot, CDN)
        context.update({
            'niwr_script': niwr_script,
            'niwr_div': niwr_div,
        })

        labor_table = data.get_derived_table("Labor", groups)
        labor_plot = plots.plot_labor_table(labor_table)
        labor_script, labor_div = components(labor_plot, CDN)
        context.update({
            'labor_script': labor_script,
            'labor_div': labor_div,
        })

        revenue_af_plot = plots.plot_revenue_af_table(revenue_table, niwr_table)
        revenue_af_script, revenue_af_div = components(revenue_af_plot, CDN)
        context.update({
            'revenue_af_script': revenue_af_script,
            'revenue_af_div': revenue_af_div,
        })
    else:
        revenue_table = data.get_table("$")

    revenue_plot = plotting.bar_plot_table(
        revenue_table,
        title='Gross Revenue ($)',
        palette=Spectral9,
        legend='bottom_right',
        xlabel='Year',
        ylabel='',
        tools=DEFAULT_TOOLS,
        logo=None,
        responsive=True,
        number_of_categories=8,
        yaxis_formatter=NumeralTickFormatter(format='$0,0')
    )
    revenue_script, revenue_div = components(revenue_plot, CDN)
    context.update({
        'revenue_script': revenue_script,
        'revenue_div': revenue_div,
    })

    cpi_data = ConsumerPriceIndexData.as_dataframe()
    revenue_table_cpi = analysis.adjust_cpi(
        revenue_table,
        bls_key,
        crop_mix.cpi_adjustment_year,
        cpi_data
    )
    revenue_cpi_plot = plotting.bar_plot_table(
        revenue_table_cpi,
        title='Gross Revenue (%s $)' % crop_mix.cpi_adjustment_year,
        palette=Spectral9,
        legend='bottom_right',
        xlabel='Year',
        ylabel='',
        tools=DEFAULT_TOOLS,
        logo=None,
        responsive=True,
        number_of_categories=8,
        yaxis_formatter=NumeralTickFormatter(format='$0,0')
    )
    revenue_cpi_script, revenue_cpi_div = components(revenue_cpi_plot, CDN)
    context.update({
        'revenue_cpi_script': revenue_cpi_script,
        'revenue_cpi_div': revenue_cpi_div,
    })

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

class EditCropMixView(EditObjectView):
    template_name = "econ/crop_mix_edit.django.html"
    model = CropMix
    form = ("cropmix", forms.CropMixForm)
    formsets = {
        "years": forms.CropMixYearFormset,
        "commodities": forms.CropMixCommodityFormset,
    }
    title = "Edit Crop Mix"
    url_name  = "crop_mix_edit"
    redirect_url_name = "crop_mix_detail"
    redirect_parameter_name =  "crop_mix_id"
    additional_context = {
        "upload_form": FileUploadForm(),
    }

class EditCropMixGroupsView(View):

    def _create_formset(self, crop_mix):
        """Creates the formset class by binding the crop_mix_data parameter
        prior to instantiation of the formset's form. This allows us to pass
        nonstandard parameters to the CropMixGroupForm constructor even though
        its instantiation is managed by the formset.
        """
        return inlineformset_factory(
            CropMix,
            CropMixGroup,
            form=bind_form_parameters(
                forms.CropMixGroupForm,
                crop_mix_data=crop_mix.get_data()[0]),
            extra=3
        )

    def get(self, request, crop_mix_id):
        crop_mix = get_object_or_404(CropMix, pk=crop_mix_id)
        CropMixGroupFormset = self._create_formset(crop_mix)
        groups_formset = CropMixGroupFormset(instance=crop_mix)
        context = {
            "title": "Edit %s Groups" % crop_mix.name,
            "year": datetime.now().year,
            "formset": groups_formset,
        }
        return render(request, "econ/crop_mix_group_edit.django.html", context)

    def post(self, request, crop_mix_id):
        crop_mix = get_object_or_404(CropMix, pk=crop_mix_id)
        CropMixGroupFormset = self._create_formset(crop_mix)
        groups_formset = CropMixGroupFormset(request.POST, instance=crop_mix)
        if groups_formset.is_valid():
            groups_formset.save()
            return redirect("crop_mix_detail", crop_mix_id=crop_mix.id)
        context = {
            "title": "Edit %s Groups" % crop_mix.name,
            "year": datetime.now().year,
            "formset": groups_formset,
        }
        return render(request, "econ/crop_mix_group_edit.django.html", context)

