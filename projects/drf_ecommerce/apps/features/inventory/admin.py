# py
# django
from django.contrib import admin # type: ignore
# drf
# third
from import_export import resources # type: ignore
from import_export.admin import ImportExportModelAdmin # type: ignore
# own
from apps.features.inventory.models import InventoryMovements, Stocks, Warehouses, WarehouseTransfers

# Register your models here.

# InventoryMovements
class InventoryMovementsResource(resources.ModelResource):
    class Meta:
        model = InventoryMovements

class InventoryMovementsAdmin(ImportExportModelAdmin):
    search_fields = ('notes',)
    list_display = ('product', 'warehouse', 'movement_type', 'sale', 'expense', 'notes', 'balance', 'quantity', 'is_active', 'created_at','updated_at','deleted_at')
    list_filter = ('product', 'warehouse', 'movement_type', 'sale', 'expense', 'is_active', 'created_at','updated_at','deleted_at')
    readonly_fields = ('created_at','updated_at','deleted_at')
    ordering = ('created_at',)
    resource_classes = (InventoryMovementsResource,)

# Stocks
class StocksResource(resources.ModelResource):
    class Meta:
        model = Stocks

class StocksAdmin(ImportExportModelAdmin):
    # search_fields = ('notes',)
    list_display = ('product', 'warehouse', 'quantity', 'is_active', 'created_at','updated_at','deleted_at')
    list_filter = ('is_active', 'created_at','updated_at','deleted_at')
    readonly_fields = ('created_at','updated_at','deleted_at')
    ordering = ('created_at',)
    resource_classes = (StocksResource,)

# Warehouses
class WarehousesResource(resources.ModelResource):
    class Meta:
        model = Warehouses

class WarehousesAdmin(ImportExportModelAdmin):
    search_fields = ('code','name','address','notes')
    list_display = ('code', 'name', 'address', 'country', 'city', 'user', 'notes', 'created_at','updated_at','deleted_at')
    list_filter = ('country', 'city', 'user', 'is_active', 'created_at','updated_at','deleted_at')
    readonly_fields = ('created_at','updated_at','deleted_at')
    ordering = ('created_at',)
    resource_classes = (WarehousesResource,)

# WarehouseTransfers
class WarehouseTransfersResource(resources.ModelResource):
    class Meta:
        model = WarehouseTransfers

class WarehouseTransfersAdmin(ImportExportModelAdmin):
    search_fields = ('notes',)
    list_display = ('product', 'origin', 'destination', 'quantity', 'notes', 'created_at','updated_at','deleted_at')
    list_filter = ('product', 'origin', 'destination', 'is_active', 'created_at','updated_at','deleted_at')
    readonly_fields = ('created_at','updated_at','deleted_at')
    ordering = ('created_at',)
    resource_classes = (WarehouseTransfersResource,)

# Registers.
admin.site.register(InventoryMovements, InventoryMovementsAdmin)
admin.site.register(Stocks, StocksAdmin)
admin.site.register(Warehouses, WarehousesAdmin)
admin.site.register(WarehouseTransfers, WarehouseTransfersAdmin)