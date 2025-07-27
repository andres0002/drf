# py
# django
from django.contrib import admin
# drf
# third
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# own
from apps.features.expense.models import (
    Suppliers, PaymentTypes, Vouchers,
    CategoriesExpense, Expenses, Mermas
)

# Register your models here.

class SuppliersResource(resources.ModelResource):
    class Meta:
        model = Suppliers

class SuppliersAdmin(ImportExportModelAdmin):
    search_fields = ('ruc', 'business_name', 'address', 'phone', 'email')
    list_display = ('ruc', 'business_name', 'address', 'phone', 'email', 'is_active', 'created_at','updated_at','deleted_at')
    list_filter = ('is_active', 'created_at','updated_at','deleted_at')
    readonly_fields = ('created_at','updated_at','deleted_at')
    ordering = ('created_at',)
    resource_classes = (SuppliersResource,)

class PaymentTypesResource(resources.ModelResource):
    class Meta:
        model = PaymentTypes

class PaymentTypesAdmin(ImportExportModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'is_active', 'created_at','updated_at','deleted_at')
    list_filter = ('is_active', 'created_at','updated_at','deleted_at')
    readonly_fields = ('created_at','updated_at','deleted_at')
    ordering = ('created_at',)
    resource_classes = (PaymentTypesResource,)

class VouchersResource(resources.ModelResource):
    class Meta:
        model = Vouchers

class VouchersAdmin(ImportExportModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'is_active', 'created_at','updated_at','deleted_at')
    list_filter = ('is_active', 'created_at','updated_at','deleted_at')
    readonly_fields = ('created_at','updated_at','deleted_at')
    ordering = ('created_at',)
    resource_classes = (VouchersResource,)

class CategoriesExpenseResource(resources.ModelResource):
    class Meta:
        model = CategoriesExpense

class CategoriesExpenseAdmin(ImportExportModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'is_active', 'created_at','updated_at','deleted_at')
    list_filter = ('is_active', 'created_at','updated_at','deleted_at')
    readonly_fields = ('created_at','updated_at','deleted_at')
    ordering = ('created_at',)
    resource_classes = (CategoriesExpenseResource,)

class ExpensesResource(resources.ModelResource):
    class Meta:
        model = Expenses

class ExpensesAdmin(ImportExportModelAdmin):
    search_fields = ('voucher_number',)
    list_display = ('voucher_number', 'date', 'quantity', 'unit_price', 'total', 'voucher', 'user', 'supplier', 'payment_type', 'product', 'is_active', 'created_at','updated_at','deleted_at')
    list_filter = ('is_active', 'created_at','updated_at','deleted_at')
    readonly_fields = ('created_at','updated_at','deleted_at')
    ordering = ('created_at',)
    resource_classes = (ExpensesResource,)

class MermasResource(resources.ModelResource):
    class Meta:
        model = Mermas

class MermasAdmin(ImportExportModelAdmin):
    search_fields = ('date',)
    list_display = ('date', 'product', 'quantity', 'is_active', 'created_at','updated_at','deleted_at')
    list_filter = ('is_active', 'created_at','updated_at','deleted_at')
    readonly_fields = ('created_at','updated_at','deleted_at')
    ordering = ('created_at',)
    resource_classes = (MermasResource,)

admin.site.register(Suppliers, SuppliersAdmin)
admin.site.register(PaymentTypes, PaymentTypesAdmin)
admin.site.register(Vouchers, VouchersAdmin)
admin.site.register(CategoriesExpense, CategoriesExpenseAdmin)
admin.site.register(Expenses, ExpensesAdmin)
admin.site.register(Mermas, MermasAdmin)