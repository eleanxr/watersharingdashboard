from django.contrib import admin

# Register your models here.
from models import GageLocation, Watershed, GradedFlowTarget, GradedFlowTargetElement
from models import Scenario, GageDataSource, ExcelDataSource, DataFile

admin.site.register(GageLocation)
admin.site.register(Watershed)
admin.site.register(Scenario)
admin.site.register(GageDataSource)
admin.site.register(ExcelDataSource)
admin.site.register(DataFile)

class GradedFlowTargetElementInline(admin.StackedInline):
    model = GradedFlowTargetElement
    extra = 3

class GradedFlowTargetAdmin(admin.ModelAdmin):
    fields = ['watershed', 'name', 'description']
    inlines = [GradedFlowTargetElementInline]
admin.site.register(GradedFlowTarget, GradedFlowTargetAdmin)
