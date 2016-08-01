from django.contrib import admin

# Register your models here.
from models import Project, HUCRegion, GISLayer
from models import ProjectScenarioRelationship, ProjectCropMixRelationship

from django.http import HttpResponseRedirect

from utils.navigation import maybe_redirect

admin.site.register(ProjectScenarioRelationship)
admin.site.register(ProjectCropMixRelationship)

class HUCRegionInline(admin.TabularInline):
    model = HUCRegion
    fields = ["hucid"]
    extra = 2

class GISLayerInline(admin.TabularInline):
    model = GISLayer
    fields = ["name", "description", "url"]
    extra = 2

class ProjectAdmin(admin.ModelAdmin):
    fields = ['watershed', 'name', 'description', 'huc_scale', 'show_project']
    inlines = [HUCRegionInline, GISLayerInline]

    def response_change(self, request, obj):
        response = super(ProjectAdmin, self).response_change(request, obj)
        return maybe_redirect(request, response, obj)

    def response_add(self, request, obj):
        response = super(ProjectAdmin, self).response_add(request, obj)
        return maybe_redirect(request, response, obj)
admin.site.register(Project, ProjectAdmin)
