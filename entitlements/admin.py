from django.contrib import admin

import models

class EntitlementInline(admin.TabularInline):
    model = models.Entitlement
    fields = [
        'name',
        'security',
        'permanence',
        'priority_date',
        'effective_date',
        'term',
        'flow_rate',
        'begin',
        'end',
    ]

class EntitlementSetInline(admin.ModelAdmin):
    fields = ['name', 'description']
    inlines = [EntitlementInline]
admin.site.register(models.EntitlementSet, EntitlementSetInline)
