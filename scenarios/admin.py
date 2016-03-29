from django.contrib import admin

from models import GageLocation, CyclicTarget, CyclicTargetElement
from models import Scenario
from django.http import HttpResponseRedirect

admin.site.register(GageLocation)

def maybe_redirect(request, response, obj):
    redirect_to_view = request.GET.get('navsource') == 'main'
    if (isinstance(response, HttpResponseRedirect) and redirect_to_view):
        response['location'] = obj.get_absolute_url()
    return response

class CyclicTargetElementInline(admin.TabularInline):
    model = CyclicTargetElement
    fields = ['target_value', 'from_month', 'from_day', 'to_month', 'to_day']
    extra = 3

class CyclicTargetAdmin(admin.ModelAdmin):
    fields = ['name', 'description']
    inlines = [CyclicTargetElementInline]
admin.site.register(CyclicTarget, CyclicTargetAdmin)

class ScenarioAdmin(admin.ModelAdmin):
    __USGS_HELP="""Information about a USGS data source. You only need to enter
    data here if you selected a source type of "USGS Gage" above."""
    __EXCEL_HELP="""Information about an excel data file. You only need to enter
    data here if you selected a source type of "Excel File" above."""

    fieldsets = (
        (None, {
            'fields': [
                'name',
                'description',
                'attribute_multiplier',
                'source_type'
            ],
        }),
        ('USGS Data', {
            'classes': ('collapse',),
            'description': __USGS_HELP,
            'fields': [
                ('gage_location', 'parameter_code', 'parameter_name'),
                ('start_date', 'end_date'),
                ('target',)
            ],
        }),
        ('Excel Data', {
            'classes': ('collapse',),
            'description': __EXCEL_HELP,
            'fields': ['excel_file', 'sheet_name', 'date_column_name', 'attribute_column_name', 'target_column_name'],
        }),
    )

    def response_change(self, request, obj):
        response = super(ScenarioAdmin, self).response_change(request, obj)
        return maybe_redirect(request, response, obj)

    def response_add(self, request, obj):
        response = super(ScenarioAdmin, self).response_add(request, obj)
        return maybe_redirect(request, response, obj)
admin.site.register(Scenario, ScenarioAdmin)
