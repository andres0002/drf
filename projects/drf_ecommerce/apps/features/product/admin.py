# py
# django
from django.contrib import admin
# drf
# third
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# own
from apps.features.product.models import MeasureUnits, CategoriesProduct, Indicators, Products

# Register your models here.

# MeasureUnits.
class MeasureUnitsResource(resources.ModelResource):
    class Meta:
        model = MeasureUnits

class MeasureUnitsAdmin(ImportExportModelAdmin):
    search_fields = ('description',)
    list_display = ('description','created_at','updated_at','deleted_at')
    list_filter = ('created_at','updated_at','deleted_at')
    readonly_fields = ('created_at','updated_at','deleted_at')
    ordering = ('created_at',)
    resource_classes = (MeasureUnitsResource,)

# CategoriesProduct.
class CategoriesProductResource(resources.ModelResource):
    class Meta:
        model = CategoriesProduct

class CategoriesProductAdmin(ImportExportModelAdmin):
    search_fields = ('description',)
    list_display = ('description','created_at','updated_at','deleted_at')
    list_filter = ('created_at','updated_at','deleted_at')
    readonly_fields = ('created_at','updated_at','deleted_at')
    ordering = ('created_at',)
    resource_classes = (CategoriesProductResource,)

# Indicators.
class IndicatorsResource(resources.ModelResource):
    class Meta:
        model = Indicators

class IndicatorsAdmin(ImportExportModelAdmin):
    search_fields = ('descount_value',)
    list_display = ('descount_value','category','created_at','updated_at','deleted_at')
    list_filter = ('descount_value','category','created_at','updated_at','deleted_at')
    readonly_fields = ('created_at','updated_at','deleted_at')
    ordering = ('created_at',)
    resource_classes = (IndicatorsResource,)

# Products.
class ProductsResource(resources.ModelResource):
    class Meta:
        model = Products

class ProductsAdmin(ImportExportModelAdmin):
    search_fields = ('name','description')
    list_display = ('name','description','measure_unit','category','created_at','updated_at','deleted_at')
    list_filter = ('measure_unit','category','created_at','updated_at','deleted_at')
    readonly_fields = ('created_at','updated_at','deleted_at')
    ordering = ('created_at',)
    resource_classes = (ProductsResource,)

# Regiters.
admin.site.register(MeasureUnits, MeasureUnitsAdmin)
admin.site.register(CategoriesProduct, CategoriesProductAdmin)
admin.site.register(Indicators, IndicatorsAdmin)
admin.site.register(Products, ProductsAdmin)