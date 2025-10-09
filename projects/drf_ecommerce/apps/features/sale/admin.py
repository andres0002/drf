# py
# django
from django.contrib import admin # type: ignore
# drf
# third
from import_export import resources # type: ignore
from import_export.admin import ImportExportModelAdmin # type: ignore
# own
from apps.features.sale.models import Customers, Sales, SaleDetails

# Register your models here.

# Customers.
class CustomersResource(resources.ModelResource):
    class Meta:
        model = Customers

class CustomersAdmin(ImportExportModelAdmin):
    # search_fields = ('description',)
    list_display = ('user','internal','document_type','document','name','lastname','email','phone','address','created_at','updated_at','deleted_at')
    list_filter = ('internal','document_type','created_at','updated_at','deleted_at')
    readonly_fields = ('created_at','updated_at','deleted_at')
    ordering = ('created_at',)
    resource_classes = (CustomersResource,)

# Sales.
class SalesResource(resources.ModelResource):
    class Meta:
        model = Sales

class SalesAdmin(ImportExportModelAdmin):
    # search_fields = ('description',)
    list_display = ('user','customer','payment_type','date','total_value','created_at','updated_at','deleted_at')
    list_filter = ('user','customer','payment_type','created_at','updated_at','deleted_at')
    readonly_fields = ('total_value', 'created_at','updated_at','deleted_at')
    ordering = ('created_at',)
    resource_classes = (SalesResource,)

# SaleDetails.
class SaleDetailsResource(resources.ModelResource):
    class Meta:
        model = SaleDetails

class SaleDetailsAdmin(ImportExportModelAdmin):
    # search_fields = ('description',)
    list_display = ('sale','product','quantity','price','subtotal_value','created_at','updated_at','deleted_at')
    list_filter = ('product','quantity','created_at','updated_at','deleted_at')
    readonly_fields = ('subtotal_value','created_at','updated_at','deleted_at')
    ordering = ('created_at',)
    resource_classes = (SaleDetailsResource,)

# Regiters.
admin.site.register(Customers, CustomersAdmin)
admin.site.register(Sales, SalesAdmin)
admin.site.register(SaleDetails, SaleDetailsAdmin)