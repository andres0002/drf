# py
# django
from django.shortcuts import get_object_or_404
# drf
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
# third
from drf_yasg.inspectors import SwaggerAutoSchema
from rest_framework_simplejwt.authentication import JWTAuthentication
# own
# from apps.features.auth_own.authentication import CustomAuthentication
from apps.core.mixins import (
    ExplicitPermissionRequiredMixin,
    AutoPermissionRequiredMixin
)

# Generar tag automatico de swagger por model.
class AutoTagSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        serializer = self.view.get_serializer_class()
        model = getattr(serializer.Meta, 'model', None)
        if model:
            return [f"🔹 {model.__name__}"]
        return ['NoTag']

class PublicGeneralViewSets(ExplicitPermissionRequiredMixin, ViewSet):
    authentication_classes = []  # <- Desactiva autenticación automática
    permission_classes = (AllowAny,)
    
    serializer_class = None
    serializer_view_class = None  # Solo para lectura.
    swagger_schema = AutoTagSchema # para definir tag por model automaticamente.
    
    def get_serializer_class(self):
        # Si es un método de solo lectura (list o retrieve), usa el serializer de vista.
        if self.action in ['list', 'retrieve'] and self.serializer_view_class:
            return self.serializer_view_class
        return self.serializer_class  # Para otros métodos (create, update, etc.).
    
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def get_queryset(self):
        # Modificar el queryset para obtener solo objects activos.
        model = self.get_serializer_class().Meta.model
        return model.objects.filter(is_active=True)
    
    # para slug se require un campo slug unico en el model.
    def get_object(self):
        queryset = self.get_queryset()
        lookup_value = self.kwargs.get('pk')

        if lookup_value.isdigit():
            lookup_field = 'pk'
        else:
            lookup_field = 'slug'

        obj = get_object_or_404(queryset, **{lookup_field: lookup_value})
        
        # 👇 Llama a permisos a nivel de objeto
        self.check_object_permissions(self.request, obj)

        return obj

class PrivateGeneralViewSets(AutoPermissionRequiredMixin, ViewSet):
    # authentication_classes = (CustomAuthentication,)
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    serializer_class = None
    serializer_view_class = None  # Solo para lectura.
    swagger_schema = AutoTagSchema # para definir tag por model automaticamente.
    
    def get_serializer_class(self):
        # Si es un método de solo lectura (list o retrieve), usa el serializer de vista.
        if self.action in ['list', 'retrieve'] and self.serializer_view_class:
            return self.serializer_view_class
        return self.serializer_class  # Para otros métodos (create, update, etc.).
    
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def get_queryset(self):
        # Modificar el queryset para obtener solo objects activos.
        model = self.get_serializer_class().Meta.model
        return model.objects.filter(is_active=True)
    
    # para slug se require un campo slug unico en el model.
    def get_object(self):
        queryset = self.get_queryset()
        lookup_value = self.kwargs.get('pk')

        if lookup_value.isdigit():
            lookup_field = 'pk'
        else:
            lookup_field = 'slug'

        obj = get_object_or_404(queryset, **{lookup_field: lookup_value})
        
        # 👇 Llama a permisos a nivel de objeto
        self.check_object_permissions(self.request, obj)

        return obj