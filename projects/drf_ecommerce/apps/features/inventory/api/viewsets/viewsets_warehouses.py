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
    WarehousesViewSerializer,
    WarehousesActionsSerializer
)

class PublicWarehousesViewSets(PublicGeneralViewSets):
    serializer_class = WarehousesActionsSerializer
    serializer_view_class = WarehousesViewSerializer
    
    def list(self, request, *args, **kwargs):
        warehouses = self.get_queryset()
        warehouses_serializer = self.get_serializer(warehouses, many = True)
        return Response(warehouses_serializer.data,status=status.HTTP_200_OK)

class PrivateWarehousesModelViewSets(PrivateGeneralModelViewSets):
    serializer_class = WarehousesActionsSerializer
    serializer_view_class = WarehousesViewSerializer

    # elimination logical. -> para elimination direct se comenta el method destroy().
    def destroy(self, request, *args, **kwargs):
        warehouse = self.get_object()
        if warehouse:
            warehouse.is_active = False
            warehouse.save()
            return Response({'message':'Successfully Warehouse elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful Warehouse elimination.'},status=status.HTTP_400_BAD_REQUEST)