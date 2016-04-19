from django import forms

from django.forms import modelform_factory, inlineformset_factory, formset_factory

from .models import CropMix, CropMixYear, CropMixCommodity
from .models import CropMixGroup, CropMixGroupItem

import views

def list_states():
    client = views.create_nass_client()
    codes = client.listvalues('state_alpha')
    return sorted(zip(codes, codes))

def list_counties():
    client = views.create_nass_client()
    codes = client.listvalues('county_name')
    return sorted(zip(codes, codes))

def list_commodities():
    client= views.create_nass_client()
    codes = client.listvalues('commodity_desc')
    return sorted(zip(codes, codes))

class CropMixForm(forms.ModelForm):

    state = forms.ChoiceField(required=True, choices=list_states)
    county = forms.ChoiceField(required=True, choices=list_counties)
    
    class Meta:
        model = CropMix
        fields = [
            'name',
            'description',
            'state',
            'county',
            'source',
            'cpi_adjustment_year',
            'source_type',
            'excel_file',
            'sheet_name',
            'year_column_name',
            'crop_column_name',
            'unit_column_name',
        ]


CropMixYearFormset = inlineformset_factory(CropMix, CropMixYear, fields=['year'], extra=0)

CropMixCommodityFormset = inlineformset_factory(CropMix, CropMixCommodity, fields=['commodity'],
    extra=0)

class CropMixGroupForm(forms.ModelForm):
    class Meta:
        model = CropMixGroup
        fields = ['group_name']

CropMixGroupItemFormset = inlineformset_factory(CropMixGroup, CropMixGroupItem, fields=['item_name'])

class CropMixGroupForm(forms.ModelForm):
    class Meta:
        model = CropMixGroup
        fields = [
            "group_name",
            "revenue",
            "labor",
            "niwr",
        ]

    items = forms.MultipleChoiceField(choices=[],
        help_text='Choose the set of commodities that should be in this group')

    def __init__(self, *args, **kwargs):
        super(CropMixGroupForm, self).__init__(*args, **kwargs)
        if self.instance:
            data, years, commodities = self.instance.analysis.get_data()
            self.fields['items'].choices = [(str(c), str(c)) 
                for c in data.data['commodity_desc'].unique()]
            self.fields['items'].initial = self.instance.cropmixgroupitem_set.all()

CropMixGroupFormset = inlineformset_factory(CropMix, CropMixGroup,
    form=CropMixGroupForm, extra=0)
