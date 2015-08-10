from django.contrib import admin

# Register your models here.
from models import GageLocation, Watershed, CyclicTarget, CyclicTargetElement
from models import Scenario, DataFile, Project



admin.site.register(GageLocation)
admin.site.register(Watershed)
admin.site.register(DataFile)
admin.site.register(Project)

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
            'fields': ['project', 'name', 'description', 'source_type'],
        }),
        ('USGS Data', {
            'classes': ('collapse',),
            'description': __USGS_HELP,
            'fields': [('gage_location', 'start_date', 'end_date', 'target')],
        }),
        ('Excel Data', {
            'classes': ('collapse',),
            'description': __EXCEL_HELP,
            'fields': ['excel_file', 'sheet_name', 'date_column_name', 'flow_column_name', 'target_column_name'],
        }),
    )
admin.site.register(Scenario, ScenarioAdmin)
