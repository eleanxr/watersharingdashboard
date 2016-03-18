from django.contrib import admin

from models import \
    CropMix,\
    CropMixYear,\
    CropMixCommodity,\
    CropMixGroup,\
    CropMixGroupItem,\
    CropMixProductionPractice,\
    ConsumerPriceIndexData,\
    ApiKey

from utils.navigation import maybe_redirect

admin.site.register(ApiKey)
admin.site.register(ConsumerPriceIndexData)

class CropMixYearInline(admin.TabularInline):
    model = CropMixYear
    fields = ['year']

class CropMixCommodityInline(admin.TabularInline):
    model = CropMixCommodity
    fields = ['commodity']

class CropMixProductionPracticeInline(admin.TabularInline):
    model = CropMixProductionPractice
    fields = ['production_practice']

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
    fieldsets = (
        (None, {
            'fields': [
                'name',
                'description',
                'state',
                'county',
                'cpi_adjustment_year',
                'source',
                'source_type',
            ],
        }),
        ("Excel File", {
            'classes': ('collapse',),
            'description': 'Information required when using an Excel data source.',
            'fields': [
                'excel_file',
                'sheet_name',
                'year_column_name',
                'crop_column_name',
                'unit_column_name',
            ]
        })
    )

    inlines = [
        CropMixYearInline,
        CropMixCommodityInline,
        CropMixProductionPracticeInline
    ]

    def response_change(self, request, obj):
        response = super(CropMixAdmin, self).response_change(request, obj)
        return maybe_redirect(request, response, obj)

    def response_add(self, request, obj):
        response = super(CropMixAdmin, self).response_add(request, obj)
        return maybe_redirect(request, response, obj)
admin.site.register(CropMix, CropMixAdmin)
