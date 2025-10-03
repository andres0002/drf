# py
# django
from django.contrib import admin # type: ignore
# drf
# third
from import_export import resources # type: ignore
from import_export.admin import ImportExportModelAdmin # type: ignore
# own
from apps.features.cart.models import Carts, CartItems

# Register your models here.

# Carts
class CartsResource(resources.ModelResource):
    class Meta:
        model = Carts

class CartsAdmin(ImportExportModelAdmin):
    # search_fields = ('notes',)
    list_display = ('user', 'status', 'total', 'is_active', 'created_at','updated_at','deleted_at')
    list_filter = ('user', 'status', 'is_active', 'created_at','updated_at','deleted_at')
    readonly_fields = ('created_at','updated_at','deleted_at')
    ordering = ('created_at',)
    resource_classes = (CartsResource,)

# CartItems
class CartItemsResource(resources.ModelResource):
    class Meta:
        model = CartItems

class CartItemsAdmin(ImportExportModelAdmin):
    # search_fields = ('notes',)
    list_display = ('cart', 'product', 'quantity', 'price', 'subtotal', 'is_active', 'created_at','updated_at','deleted_at')
    list_filter = ('cart', 'product', 'is_active', 'created_at','updated_at','deleted_at')
    readonly_fields = ('created_at','updated_at','deleted_at')
    ordering = ('created_at',)
    resource_classes = (CartItemsResource,)

# Registers.
admin.site.register(Carts, CartsAdmin)
admin.site.register(CartItems, CartItemsAdmin)