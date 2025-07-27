# py
# django
from django.contrib.auth import get_permission_codename
# drf
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
# third
from drf_yasg.utils import swagger_auto_schema # type: ignore
# own

class ExplicitPermissionRequiredMixin:
    """
    Mixin para ViewSets de DRF que permite definir permisos explícitos por acción
    usando un diccionario `permission_required`.

    - is_superuser: acceso total
    - is_staff + is_active: deben tener el permiso definido en `permission_required`
    - otros: denegado
    - Si no se define un permiso para la acción, permite la acción (comportamiento opcional)
    """

    permission_required = {
        # 'list':    '{app_label}.view_{model_name}' or ['{app_label}.view_{model_name}'],
        # 'retrieve': '{app_label}.view_{model_name}' or ['{app_label}.view_{model_name}'],
        # 'create':  '{app_label}.add_{model_name}' or ['{app_label}.add_{model_name}'],
        # 'update':  '{app_label}.change_{model_name}' or ['{app_label}.change_{model_name}'],
        # 'partial_update': '{app_label}.change_{model_name}' or ['{app_label}.change_{model_name}'],
        # 'destroy': '{app_label}.delete_{model_name}' or ['{app_label}.delete_{model_name}'],
    }
    
    def _format_permission(self, perm_string):
        """
        Reemplaza {app_label} y {model_name} en el string del permiso.
        """
        model = getattr(getattr(self, 'queryset', None), 'model', None)
        if not model:
            return perm_string

        return perm_string.format(
            app_label=model._meta.app_label,
            model_name=model._meta.model_name
        )
    
    def get_required_permissions(self):
        """
        Reemplaza los placeholders {app_label} y {model_name} con valores reales.
        """
        raw_perm = self.permission_required.get(self.action)

        if not raw_perm:
            return None

        # Si es una lista de permisos
        if isinstance(raw_perm, list):
            return [self._format_permission(p) for p in raw_perm]

        return [self._format_permission(raw_perm)]

    def has_action_permission(self):
        user = self.request.user
        
        # Acciones de solo lectura (permitidas para todos)
        if self.action in ['list', 'retrieve']:
            return True

        if user.is_authenticated and user.is_superuser and user.is_active:
            return True
        
        perms = self.get_required_permissions()
        if not perms:
            return True  # Si no hay permisos definidos, permite

        # Acciones protegidas: requieren permisos explícitos
        if user.is_authenticated and user.is_staff and user.is_active:
            if isinstance(perms, str):
                perms = [perms]
            return user.has_perms(perms)

        return False

    def initial(self, request, *args, **kwargs):
        if not self.has_action_permission():
            raise PermissionDenied("No tienes permiso para realizar esta acción.")
        super().initial(request, *args, **kwargs)

class AutoPermissionRequiredMixin:
    """
    Mixin para ModelViewSet que infiere automáticamente permisos requeridos
    según la acción y el modelo asociado.

    - Definir permisos por acción con placeholders {app_label} y {model_name}
    - Aplica permisos automáticos (view, add, change, delete).
    - Suma permisos definidos en `permission_required` por acción.
    - Usa `__permission_required_custom` internamente si se desea extender.
    - is_superuser: acceso total
    - is_staff + is_active: deben tener el permiso inferido
    - otros: acceso denegado
    """
    
    # para custom que se quieren para un model en especifico.
    permission_required = {
        # 'list':    '{app_label}.view_{model_name}' or ['{app_label}.view_{model_name}'],
        # 'retrieve': '{app_label}.view_{model_name}' or ['{app_label}.view_{model_name}'],
        # 'create':  '{app_label}.add_{model_name}' or ['{app_label}.add_{model_name}'],
        # 'update':  '{app_label}.change_{model_name}' or ['{app_label}.change_{model_name}'],
        # 'partial_update': '{app_label}.change_{model_name}' or ['{app_label}.change_{model_name}'],
        # 'destroy': '{app_label}.delete_{model_name}' or ['{app_label}.delete_{model_name}'],
    }
    
    # para custom que se quieren desde un inicio o por default.
    __permission_required_custom = {
        # 'list':    '{app_label}.view_{model_name}' or ['{app_label}.view_{model_name}'],
        # 'retrieve': '{app_label}.view_{model_name}' or ['{app_label}.view_{model_name}'],
        # 'create':  '{app_label}.add_{model_name}' or ['{app_label}.add_{model_name}'],
        # 'update':  '{app_label}.change_{model_name}' or ['{app_label}.change_{model_name}'],
        # 'partial_update': '{app_label}.change_{model_name}' or ['{app_label}.change_{model_name}'],
        # 'destroy': '{app_label}.delete_{model_name}' or ['{app_label}.delete_{model_name}'],
    }

    def _format_permission(self, perm_string):
        """
        Reemplaza {app_label} y {model_name} en un string de permiso.
        """
        model = getattr(getattr(self, 'queryset', None), 'model', None)
        if not model:
            return perm_string

        return perm_string.format(
            app_label=model._meta.app_label,
            model_name=model._meta.model_name
        )
    
    def _get_automatic_permission(self):
        action_map = {
            'list': 'view',
            'retrieve': 'view',
            'create': 'add',
            'update': 'change',
            'partial_update': 'change',
            'destroy': 'delete',
        }

        model = getattr(getattr(self, 'queryset', None), 'model', None)
        if not model:
            return []

        perm_type = action_map.get(self.action)
        if not perm_type:
            return []

        codename = get_permission_codename(perm_type, model._meta)
        return [f"{model._meta.app_label}.{codename}"]

    def get_required_permissions(self):
        perms = self._get_automatic_permission()

        # Agregar permisos definidos públicamente por el desarrollador
        raw_public = self.permission_required.get(self.action)
        if raw_public:
            if isinstance(raw_public, list):
                perms += [self._format_permission(p) for p in raw_public]
            else:
                perms.append(self._format_permission(raw_public))

        # Agregar permisos personalizados internos del mixin
        raw_internal = self.__permission_required_custom.get(self.action)
        if raw_internal:
            if isinstance(raw_internal, list):
                perms += [self._format_permission(p) for p in raw_internal]
            else:
                perms.append(self._format_permission(raw_internal))

        return perms

    def has_action_permission(self):
        user = self.request.user

        if user.is_authenticated and user.is_superuser and user.is_active:
            return True

        if user.is_authenticated and user.is_staff and user.is_active:
            perms = self.get_required_permissions()
            if not perms:
                return False  # No hay permisos definidos para esta acción -> denegar
            return user.has_perms(perms)

        return False

    def initial(self, request, *args, **kwargs):
        if not self.has_action_permission():
            raise PermissionDenied("No tienes permiso para realizar esta acción.")
        return super().initial(request, *args, **kwargs)

class BulkDeleteLogicalAndDirectDisabledMixin:
    @swagger_auto_schema(
        method='delete',
        request_body=None,  # No se espera un body, ya que está deshabilitado
        responses={405: 'Method Not Allowed'},
        operation_summary="❌ Este endpoint está deshabilitado para este recurso.", # comment endpoint.
        operation_description="❌ Este endpoint está deshabilitado para este recurso.",
        auto_schema=None  # <- Evita heredar o construir automáticamente respuestas previas
    )
    # Deshabilitar el action bulk_delete_logical
    @action(detail=False, methods=['delete'], url_path='bulk_delete_logical')
    def bulk_delete_logical(self, request):
        return Response({'detail': 'This action is not allowed on this view.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @swagger_auto_schema(
        method='delete',
        request_body=None,  # No se espera un body, ya que está deshabilitado
        responses={405: 'Method Not Allowed'},
        operation_summary="❌ Este endpoint está deshabilitado para este recurso.", # comment endpoint.
        operation_description="❌ Este endpoint está deshabilitado para este recurso.",
        auto_schema=None  # <- Evita heredar o construir automáticamente respuestas previas
    )
    # Deshabilitar el action bulk_delete_direct
    @action(detail=False, methods=['delete'], url_path='bulk_delete_direct')
    def bulk_delete_direct(self, request):
        return Response({'detail': 'This action is not allowed on this view.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)