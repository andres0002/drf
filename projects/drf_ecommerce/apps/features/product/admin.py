# py
# django
from django.contrib import admin # type: ignore
# drf
# third
from import_export import resources # type: ignore
from import_export.admin import ImportExportModelAdmin # type: ignore
# own
from apps.features.product.models import MeasureUnits, ProductCategories, Promotions, Products, ProductComponents

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
class ProductCategoriesResource(resources.ModelResource):
    class Meta:
        model = ProductCategories

class ProductCategoriesAdmin(ImportExportModelAdmin):
    search_fields = ('description',)
    list_display = ('description','created_at','updated_at','deleted_at')
    list_filter = ('created_at','updated_at','deleted_at')
    readonly_fields = ('created_at','updated_at','deleted_at')
    ordering = ('created_at',)
    resource_classes = (ProductCategoriesResource,)

# Promotions.
class PromotionsResource(resources.ModelResource):
    class Meta:
        model = Promotions

class PromotionsAdmin(ImportExportModelAdmin):
    search_fields = ('name','description')
    list_display = ('name','description','discount_type','discount_value','start_date','end_date','is_valid','created_at','updated_at','deleted_at')
    list_filter = ('discount_type','start_date','end_date','created_at','updated_at','deleted_at')
    readonly_fields = ('is_valid','created_at','updated_at','deleted_at')
    ordering = ('created_at',)
    resource_classes = (PromotionsResource,)

# Products.
class ProductsResource(resources.ModelResource):
    class Meta:
        model = Products

class ProductsAdmin(ImportExportModelAdmin):
    search_fields = ('name','description')
    list_display = ('name','description','measure_unit','category','is_digital','created_at','updated_at','deleted_at')
    list_filter = ('measure_unit','category','is_digital','created_at','updated_at','deleted_at')
    readonly_fields = ('suggested_price_display','created_at','updated_at','deleted_at')
    ordering = ('created_at',)
    resource_classes = (ProductsResource,)
    
    def suggested_price_display(self, obj):
        return obj.suggested_price
    suggested_price_display.short_description = "Suggested Price"

# ProductComponents.
class ProductComponentsResource(resources.ModelResource):
    class Meta:
        model = ProductComponents

class ProductComponentsAdmin(ImportExportModelAdmin):
    # search_fields = ('name','description')
    list_display = ('product','subproduct','measure_unit','quantity','created_at','updated_at','deleted_at')
    list_filter = ('product','subproduct','measure_unit','created_at','updated_at','deleted_at')
    readonly_fields = ('created_at','updated_at','deleted_at')
    ordering = ('created_at',)
    resource_classes = (ProductComponentsResource,)

# Regiters.
admin.site.register(MeasureUnits, MeasureUnitsAdmin)
admin.site.register(ProductCategories, ProductCategoriesAdmin)
admin.site.register(Promotions, PromotionsAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(ProductComponents, ProductComponentsAdmin)