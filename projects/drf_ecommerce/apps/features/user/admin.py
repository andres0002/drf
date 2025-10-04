# py
# django
from django.contrib import admin # type: ignore
from django.contrib.auth.models import Permission # type: ignore
from django.contrib.contenttypes.models import ContentType # type: ignore
# third
from import_export import resources # type: ignore
from import_export.admin import ImportExportModelAdmin # type: ignore
# own
from apps.features.user.models import Users, Roles, Fingerprints, AccessLogs

# Register your models here.

# Roles
class RolesResource(resources.ModelResource):
    class Meta:
        model = Roles

class RolesAdmin(ImportExportModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'is_active', 'created_at','updated_at','deleted_at')
    list_filter = ('is_active', 'created_at','updated_at','deleted_at')
    readonly_fields = ('created_at','updated_at','deleted_at')
    ordering = ('created_at',)
    resource_classes = (RolesResource,)

# Users.
class UsersResource(resources.ModelResource):
    class Meta:
        model = Users

class UsersAdmin(ImportExportModelAdmin):
    search_fields = ('username','email','name','lastname','is_active','is_staff','is_superuser')
    list_display = ('username','email','name','lastname','is_active','is_staff','is_superuser','created_at','updated_at','deleted_at')
    list_filter = ('is_active','is_staff','is_superuser','created_at','updated_at','deleted_at')
    readonly_fields = ('created_at','updated_at','deleted_at')
    resource_classes = (UsersResource,)

# Fingerprints.
class FingerPrintsResource(resources.ModelResource):
    class Meta:
        model = Fingerprints

class FingerPrintsAdmin(ImportExportModelAdmin):
    # search_fields = ('field_name',)
    list_display = ('user','finger','template','device_serial_number','is_active','created_at','updated_at','deleted_at')
    list_filter = ('user','device_serial_number','is_active','created_at','updated_at','deleted_at')
    readonly_fields = ('created_at','updated_at','deleted_at')
    resource_classes = (FingerPrintsResource,)

# AccessLogs.
class AccessLogsResource(resources.ModelResource):
    class Meta:
        model = AccessLogs

class AccessLogsAdmin(ImportExportModelAdmin):
    search_fields = ('device_serial_number','notes')
    list_display = ('user','fingerprint','device_serial_number','verified','access_type','timestamp','notes','is_active','created_at','updated_at','deleted_at')
    list_filter = ('user','fingerprint','device_serial_number','verified','access_type','timestamp','is_active','created_at','updated_at','deleted_at')
    readonly_fields = ('created_at','updated_at','deleted_at')
    resource_classes = (AccessLogsResource,)

# Registers.
admin.site.register(Roles, RolesAdmin)
admin.site.register(Users, UsersAdmin)
admin.site.register(Fingerprints, FingerPrintsAdmin)
admin.site.register(AccessLogs, AccessLogsAdmin)
admin.site.register(Permission)
admin.site.register(ContentType)