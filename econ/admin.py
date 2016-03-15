from django.contrib import admin

from models import \
    CropMix,\
    CropMixYear,\
    CropMixCommodity,\
    CropMixGroup,\
    CropMixGroupItem,\
    ApiKey

from utils.navigation import maybe_redirect

admin.site.register(ApiKey)

class CropMixYearInline(admin.TabularInline):
    model = CropMixYear
    fields = ['year']

class CropMixCommodityInline(admin.TabularInline):
    model = CropMixCommodity
    fields = ['commodity']

class CropMixGroupItemInline(admin.TabularInline):
    model = CropMixGroupItem
    fields = ['item_name']

class CropMixGroupAdmin(admin.ModelAdmin):
    fields = [
        'analysis',
        'group_name',
        'revenue',
        'labor',
        'niwr',
    ]
    inlines = [CropMixGroupItemInline]
admin.site.register(CropMixGroup, CropMixGroupAdmin)

class CropMixAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'description',
        'state',
        'county',
        'cpi_adjustment_year',
        'source'
    ]
    inlines = [CropMixYearInline, CropMixCommodityInline]

    def response_change(self, request, obj):
        response = super(CropMixAdmin, self).response_change(request, obj)
        return maybe_redirect(request, response, obj)

    def response_add(self, request, obj):
        response = super(CropMixAdmin, self).response_add(request, obj)
        return maybe_redirect(request, response, obj)
admin.site.register(CropMix, CropMixAdmin)
