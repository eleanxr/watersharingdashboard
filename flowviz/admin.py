from django.contrib import admin

# Register your models here.
from models import Project, HUCRegion, GISLayer, ProjectScenarioRelationship

from django.http import HttpResponseRedirect

admin.site.register(ProjectScenarioRelationship)

def maybe_redirect(request, response, obj):
    redirect_to_view = request.GET.get('navsource') == 'main'
    if (isinstance(response, HttpResponseRedirect) and redirect_to_view):
        response['location'] = obj.get_absolute_url()
    return response

class HUCRegionInline(admin.TabularInline):
    model = HUCRegion
    fields = ["hucid"]
    extra = 2

class GISLayerInline(admin.TabularInline):
    model = GISLayer
    fields = ["name", "description", "url"]
    extra = 2

class ProjectAdmin(admin.ModelAdmin):
    fields = ['watershed', 'name', 'description', 'huc_scale']
    inlines = [HUCRegionInline, GISLayerInline]

    def response_change(self, request, obj):
        response = super(ProjectAdmin, self).response_change(request, obj)
        return maybe_redirect(request, response, obj)

    def response_add(self, request, obj):
        response = super(ProjectAdmin, self).response_add(request, obj)
        return maybe_redirect(request, response, obj)
admin.site.register(Project, ProjectAdmin)
