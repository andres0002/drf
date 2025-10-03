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
from apps.features.inventory.api.serializers.serializers import (
    InventoryMovementsViewSerializer,
    InventoryMovementsActionsSerializer
)

class PublicInventoryMovementsViewSets(PublicGeneralViewSets):
    serializer_class = InventoryMovementsActionsSerializer
    serializer_view_class = InventoryMovementsViewSerializer
    
    def list(self, request, *args, **kwargs):
        inventory_movements = self.get_queryset()
        inventory_movements_serializer = self.get_serializer(inventory_movements, many = True)
        return Response(inventory_movements_serializer.data,status=status.HTTP_200_OK)

class PrivateInventoryMovementsModelViewSets(PrivateGeneralModelViewSets):
    serializer_class = InventoryMovementsActionsSerializer
    serializer_view_class = InventoryMovementsViewSerializer

    # elimination logical. -> para elimination direct se comenta el method destroy().
    def destroy(self, request, *args, **kwargs):
        inventory_movement = self.get_object()
        if inventory_movement:
            inventory_movement.is_active = False
            inventory_movement.save()
            return Response({'message':'Successfully Inventory Movement elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful Inventory Movement elimination.'},status=status.HTTP_400_BAD_REQUEST)