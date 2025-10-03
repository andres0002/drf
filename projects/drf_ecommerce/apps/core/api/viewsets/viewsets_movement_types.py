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
from apps.core.api.serializers.serializers import (
    MovementTypesViewSerializer,
    MovementTypesActionsSerializer
)

class PublicMovementTypesViewSets(PublicGeneralViewSets):
    serializer_class = MovementTypesActionsSerializer
    serializer_view_class = MovementTypesViewSerializer
    
    def list(self, request, *args, **kwargs):
        movement_types = self.get_queryset()
        movement_types_serializer = self.get_serializer(movement_types, many = True)
        return Response(movement_types_serializer.data,status=status.HTTP_200_OK)

class PrivateMovementTypesModelViewSets(PrivateGeneralModelViewSets):
    serializer_class = MovementTypesActionsSerializer
    serializer_view_class = MovementTypesViewSerializer

    # elimination logical. -> para elimination direct se comenta el method destroy().
    def destroy(self, request, *args, **kwargs):
        movement_type = self.get_object()
        if movement_type:
            movement_type.is_active = False
            movement_type.save()
            return Response({'message':'Successfully Movement Type elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful Movement Type elimination.'},status=status.HTTP_400_BAD_REQUEST)