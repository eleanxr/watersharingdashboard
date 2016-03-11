from django.contrib import admin

from models import CropMix, CropMixYear, CropMixCommodity, ApiKey

from utils.navigation import maybe_redirect

admin.site.register(ApiKey)

class CropMixYearInline(admin.TabularInline):
    model = CropMixYear
    fields = ['year']

class CropMixCommodityInline(admin.TabularInline):
    model = CropMixCommodity
    fields = ['commodity']

class CropMixAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'state', 'county', 'source']
    inlines = [CropMixYearInline, CropMixCommodityInline]

    def response_change(self, request, obj):
        response = super(CropMixAdmin, self).response_change(request, obj)
        return maybe_redirect(request, response, obj)

    def response_add(self, request, obj):
        response = super(CropMixAdmin, self).response_add(request, obj)
        return maybe_redirect(request, response, obj)
admin.site.register(CropMix, CropMixAdmin)
