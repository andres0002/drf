# py
# django
# drf
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
# thrid
# own
from apps.core.api.viewsets.viewsets import (
    PublicGeneralViewSets,
    PrivateGeneralModelViewSets
)
from apps.features.user.api.serializers.serializers import (
    RolesViewSerializer,
    RolesActionsSerializer
)

class PublicRolesViewSets(PublicGeneralViewSets):
    serializer_class = RolesActionsSerializer
    serializer_view_class = RolesViewSerializer
    
    def list(self, request, *args, **kwargs):
        roles = self.get_queryset()
        roles_serializer = self.get_serializer(roles, many = True)
        return Response(roles_serializer.data,status=status.HTTP_200_OK)

class PrivateRolesModelViewSets(PrivateGeneralModelViewSets):
    serializer_class = RolesActionsSerializer
    serializer_view_class = RolesViewSerializer

    # elimination logical. -> para elimination direct se comenta el method destroy().
    def destroy(self, request, *args, **kwargs):
        role = self.get_object()
        if role:
            role.is_active = False
            role.save()
            return Response({'message':'Successfully Role elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful Role elimination.'},status=status.HTTP_400_BAD_REQUEST)