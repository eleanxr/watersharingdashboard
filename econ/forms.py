from django import forms

from django.forms import modelform_factory, inlineformset_factory, formset_factory

from .models import CropMix, CropMixYear, CropMixCommodity
from .models import CropMixGroup, CropMixGroupItem
from .models import create_nass_client

from functools import partial, wraps

def list_states():
    client = create_nass_client()
    codes = client.listvalues('state_alpha')
    return sorted(zip(codes, codes))

def list_counties():
    client = create_nass_client()
    codes = client.listvalues('county_name')
    return sorted(zip(codes, codes))

def list_commodities():
    client= create_nass_client()
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
        crop_mix_data = kwargs.pop('crop_mix_data')
        super(CropMixGroupForm, self).__init__(*args, **kwargs)
        self.fields['items'].choices = [(str(c), str(c)) 
            for c in crop_mix_data.data['commodity_desc'].unique()]
        if self.instance:
            self.fields['items'].initial = self.instance.cropmixgroupitem_set.all()

    def save(self, commit=True):
        """Calls the superclass save and saves the crop mix group items."""
        # We have to commit the save of any new groups to form valid
        # relationships between the groups and their group items with good
        # foreign keys. I'd like to find a better way to do this that respects
        # the commit argument, but I couldn't find a way to do this using the
        # current model form set infrastructure.
        instance = super(CropMixGroupForm, self).save(commit=True)
        new_items = self.cleaned_data['items']
        instance.cropmixgroupitem_set.set([
            CropMixGroupItem(item_name=name)
            for name in new_items
        ], bulk=False)
        return instance

