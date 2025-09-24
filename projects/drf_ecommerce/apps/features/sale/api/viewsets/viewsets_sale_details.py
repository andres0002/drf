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
from apps.features.sale.api.serializers.serializers import (
    SaleDetailsViewSerializer,
    SaleDetailsActionsSerializer
)

class PublicSaleDetailsViewSets(PublicGeneralViewSets):
    serializer_class = SaleDetailsActionsSerializer
    serializer_view_class = SaleDetailsViewSerializer
    
    def list(self, request, *args, **kwargs):
        sale_details = self.get_queryset()
        sale_details_serializer = self.get_serializer(sale_details, many = True)
        return Response(sale_details_serializer.data,status=status.HTTP_200_OK)

class PrivateSaleDetailsModelViewSets(PrivateGeneralModelViewSets):
    serializer_view_class = SaleDetailsViewSerializer
    serializer_class = SaleDetailsActionsSerializer

    # elimination logical. -> para elimination direct se comenta el method destroy().
    def destroy(self, request, *args, **kwargs):
        sale_detail = self.get_object()
        if sale_detail:
            sale_detail.is_active = False
            sale_detail.save()
            return Response({'message':'Successfully Sale Detail elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful Sale Detail elimination.'},status=status.HTTP_400_BAD_REQUEST)