from django.contrib import admin
from .models import Email, Sector, Campaign


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
    list_display = ('address', 'created_on')
    list_filter = ['created_on', 'sector']
    search_fields = ['address']

admin.site.register(Email, EmailAdmin)


class CampaignAdmin(admin.ModelAdmin):
    fields = ['title', 'from_email', 'html_mail', 'tags', 'created_on', 'modified_on']
    readonly_fields = ('created_on', 'modified_on')
    list_display = ('title', 'from_email', 'created_on')
    list_filter = ['created_on', 'from_email']
    search_fields = ['title', 'tags']

admin.site.register(Campaign, CampaignAdmin)
