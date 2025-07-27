# py
# django
# drf
from rest_framework.response import Response
from rest_framework import status
# third
# own
from apps.core.api.viewsets.viewsets import (
    PublicGeneralViewSets,
    PrivateGeneralModelViewSets
)
from apps.core.mixins import BulkDeleteLogicalAndDirectDisabledMixin
from apps.features.user.api.serializers.serializers import (
    UserPermissionsViewSerializer,
    UserPermissionsActionsSerializer
)

# Create your views here.

class PublicUserPermissionsViewSets(PublicGeneralViewSets):
    serializer_class = UserPermissionsActionsSerializer
    serializer_view_class = UserPermissionsViewSerializer
    
    def get_queryset(self):
        model = self.get_serializer_class().Meta.model
        return model.objects.all()
    
    def list(self, request, *args, **kwargs):
        permissions = self.get_queryset()
        permissions_serializer = self.get_serializer(permissions, many = True)
        return Response(permissions_serializer.data,status=status.HTTP_200_OK)

class PrivateUserPermissionsModelViewSets(BulkDeleteLogicalAndDirectDisabledMixin, PrivateGeneralModelViewSets):
    serializer_view_class = UserPermissionsViewSerializer
    serializer_class = UserPermissionsActionsSerializer
    
    def get_queryset(self):
        model = self.get_serializer().Meta.model
        return model.objects.all()