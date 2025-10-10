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
    WarehouseTransfersViewSerializer,
    WarehouseTransfersActionsSerializer
)

class PublicWarehouseTransfersViewSets(PublicGeneralViewSets):
    serializer_class = WarehouseTransfersActionsSerializer
    serializer_view_class = WarehouseTransfersViewSerializer
    
    def list(self, request, *args, **kwargs):
        warehouse_transfers = self.get_queryset()
        warehouse_transfers_serializer = self.get_serializer(warehouse_transfers, many = True)
        return Response(warehouse_transfers_serializer.data,status=status.HTTP_200_OK)

class PrivateWarehouseTransfersModelViewSets(PrivateGeneralModelViewSets):
    serializer_class = WarehouseTransfersActionsSerializer
    serializer_view_class = WarehouseTransfersViewSerializer

    # elimination logical. -> para elimination direct se comenta el method destroy().
    def destroy(self, request, *args, **kwargs):
        warehouse_transfer = self.get_object()
        if warehouse_transfer:
            warehouse_transfer.is_active = False
            warehouse_transfer.save()
            return Response({'message':'Successfully Warehouse Transfer elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful Warehouse Transfer elimination.'},status=status.HTTP_400_BAD_REQUEST)