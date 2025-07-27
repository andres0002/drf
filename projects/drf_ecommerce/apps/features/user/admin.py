# py
# django
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
# third
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# own
from apps.features.user.models import Users

# Register your models here.

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

# Registers.
admin.site.register(Users, UsersAdmin)
admin.site.register(Permission)
admin.site.register(ContentType)