from django.contrib import admin
from .models import Email, Sector


class SectorInline(admin.TabularInline):
    model = Sector


class EmailAdmin(admin.ModelAdmin):
    inlines = [SectorInline]
    fields = ['address', 'sector', 'created_on', 'modified_on']
    readonly_fields = ('created_on', 'modified_on')
    list_display = ('address', 'kind', 'created_on')
    list_filter = ['sector__name', 'created_on']
    search_fields = ['sector__name', 'address']

admin.site.register(Email, EmailAdmin)
