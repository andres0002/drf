# py
# django
from django.contrib import admin
# drf
# third
from import_export import resources # type: ignore
from import_export.admin import ImportExportModelAdmin # type: ignore
# own
from apps.shared.models import (
    Countries, Cities
)

# Register your models here.

# Countries.
class CountriesResource(resources.ModelResource):
    class Meta:
        model = Countries

class CountriesAdmin(ImportExportModelAdmin):
    search_fields = ('code', 'name')
    list_display = ('code', 'name', 'is_active', 'created_at','updated_at','deleted_at')
    list_filter = ('is_active', 'created_at','updated_at','deleted_at')
    readonly_fields = ('created_at','updated_at','deleted_at')
    ordering = ('created_at',)
    resource_classes = (CountriesResource,)

# Cities.
class CitiesResource(resources.ModelResource):
    class Meta:
        model = Cities

class CitiesAdmin(ImportExportModelAdmin):
    search_fields = ('code', 'name')
    list_display = ('code', 'name', 'country', 'is_active', 'created_at','updated_at','deleted_at')
    list_filter = ('country', 'is_active', 'created_at','updated_at','deleted_at')
    readonly_fields = ('created_at','updated_at','deleted_at')
    ordering = ('created_at',)
    resource_classes = (CitiesResource,)

# Registers.
admin.site.register(Countries, CountriesAdmin)
admin.site.register(Cities, CitiesAdmin)