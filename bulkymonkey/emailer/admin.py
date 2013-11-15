from django.contrib import admin
from .models import Email, Sector


class SectorAdmin(admin.ModelAdmin):
    model = Sector
    fields = ['name', 'created_on', 'modified_on']
    readonly_fields = ('created_on', 'modified_on')
    list_display = ('name', 'num_emails', 'created_on')
    search_fields = ['name']

admin.site.register(Sector, SectorAdmin)


class EmailAdmin(admin.ModelAdmin):
    fields = ['address', 'sector', 'created_on', 'modified_on']
    readonly_fields = ('created_on', 'modified_on')
    list_display = ('address', 'sector', 'created_on')
    list_filter = ['created_on', 'sector']
    search_fields = ['address']

admin.site.register(Email, EmailAdmin)
