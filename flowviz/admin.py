from django.contrib import admin

# Register your models here.
from models import GageLocation, Watershed, GradedFlowTarget, GradedFlowTargetElement

admin.site.register(GageLocation)
admin.site.register(Watershed)
# admin.site.register(GradedFlowTargetElement)

class GradedFlowTargetElementInline(admin.StackedInline):
    model = GradedFlowTargetElement
    extra = 3

class GradedFlowTargetAdmin(admin.ModelAdmin):
    fields = ['location', 'name']
    inlines = [GradedFlowTargetElementInline]
    
admin.site.register(GradedFlowTarget, GradedFlowTargetAdmin)