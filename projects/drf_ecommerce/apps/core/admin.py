# py
# django
from django.contrib import admin # type: ignore
# drf
# third
from import_export import resources # type: ignore
from import_export.admin import ImportExportModelAdmin # type: ignore
# own
from apps.core.models import (
    PaymentTypes, DocumentTypes
)

# Register your models here.

class DocumentTypesResource(resources.ModelResource):
    class Meta:
        model = DocumentTypes

class DocumentTypesAdmin(ImportExportModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'is_active', 'created_at','updated_at','deleted_at')
    list_filter = ('is_active', 'created_at','updated_at','deleted_at')
    readonly_fields = ('created_at','updated_at','deleted_at')
    ordering = ('created_at',)
    resource_classes = (DocumentTypesResource,)

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

admin.site.register(DocumentTypes, DocumentTypesAdmin)
admin.site.register(PaymentTypes, PaymentTypesAdmin)