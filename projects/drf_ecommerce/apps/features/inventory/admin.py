# py
# django
from django.contrib import admin # type: ignore
# drf
# third
from import_export import resources # type: ignore
from import_export.admin import ImportExportModelAdmin # type: ignore
# own
from apps.features.inventory.models import InventoryMovements, Stocks

# Register your models here.

# InventoryMovements
class InventoryMovementsResource(resources.ModelResource):
    class Meta:
        model = InventoryMovements

class InventoryMovementsAdmin(ImportExportModelAdmin):
    search_fields = ('notes',)
    list_display = ('notes', 'balance', 'quantity', 'is_active', 'created_at','updated_at','deleted_at')
    list_filter = ('is_active', 'created_at','updated_at','deleted_at')
    readonly_fields = ('created_at','updated_at','deleted_at')
    ordering = ('created_at',)
    resource_classes = (InventoryMovementsResource,)

# Stocks
class StocksResource(resources.ModelResource):
    class Meta:
        model = Stocks

class StocksAdmin(ImportExportModelAdmin):
    # search_fields = ('notes',)
    list_display = ('product', 'quantity', 'is_active', 'created_at','updated_at','deleted_at')
    list_filter = ('is_active', 'created_at','updated_at','deleted_at')
    readonly_fields = ('created_at','updated_at','deleted_at')
    ordering = ('created_at',)
    resource_classes = (StocksResource,)

# Registers.
admin.site.register(InventoryMovements, InventoryMovementsAdmin)
admin.site.register(Stocks, StocksAdmin)