from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.


class BroadwayDataAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = (('shows_names','shows_links'))
    search_fields = ['shows_names','shows_links']
admin.site.register(BroadwayData, BroadwayDataAdmin)