from django import forms

from django.forms import modelform_factory, inlineformset_factory, formset_factory

from .models import CropMix, CropMixYear, CropMixCommodity
from .models import CropMixGroup, CropMixGroupItem

class CropMixForm(forms.ModelForm):
    class Meta:
        model = CropMix
        fields = [
            'name',
            'description',
            'state',
            'county',
            'source',
            'cpi_adjustment_year',
        ]


CropMixYearFormset = inlineformset_factory(CropMix, CropMixYear, fields=['year'])

CropMixCommodityFormset = inlineformset_factory(CropMix, CropMixCommodity, fields=['commodity'])

class CropMixGroupForm(forms.ModelForm):
    class Meta:
        model = CropMixGroup
        fields = ['group_name']

CropMixGroupItemFormset = inlineformset_factory(CropMixGroup, CropMixGroupItem, fields=['item_name'])

CropMixGroupFormset = formset_factory(CropMixGroupForm)
