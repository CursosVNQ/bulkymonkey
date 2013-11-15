from django.contrib import admin
from .models import Email


class EmailAdmin(admin.ModelAdmin):
    fields = ['address', 'kind', 'created_on', 'modified_on']
    readonly_fields = ('created_on', 'modified_on')
    list_display = ('address', 'kind', 'created_on')
    list_filter = ['kind', 'created_on']
    search_fields = ['kind', 'address']

admin.site.register(Email, EmailAdmin)
