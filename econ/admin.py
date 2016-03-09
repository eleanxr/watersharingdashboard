from django.contrib import admin

from models import CropMix, CropMixYear, CropMixCommodity, NASSApiKey

admin.site.register(NASSApiKey)

class CropMixYearInline(admin.TabularInline):
    model = CropMixYear
    fields = ['year']

class CropMixCommodityInline(admin.TabularInline):
    model = CropMixCommodity
    fields = ['commodity']

class CropMixAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'state', 'county', 'source']
    inlines = [CropMixYearInline, CropMixCommodityInline]
admin.site.register(CropMix, CropMixAdmin)
