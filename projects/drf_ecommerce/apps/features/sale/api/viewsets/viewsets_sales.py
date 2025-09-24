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
    SalesViewSerializer,
    SalesActionsSerializer
)

class PublicSalesViewSets(PublicGeneralViewSets):
    serializer_class = SalesActionsSerializer
    serializer_view_class = SalesViewSerializer
    
    def list(self, request, *args, **kwargs):
        sales = self.get_queryset()
        sales_serializer = self.get_serializer(sales, many = True)
        return Response(sales_serializer.data,status=status.HTTP_200_OK)

class PrivateSalesModelViewSets(PrivateGeneralModelViewSets):
    serializer_view_class = SalesViewSerializer
    serializer_class = SalesActionsSerializer

    # elimination logical. -> para elimination direct se comenta el method destroy().
    def destroy(self, request, *args, **kwargs):
        sale = self.get_object()
        if sale:
            sale.is_active = False
            sale.save()
            return Response({'message':'Successfully Sale elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful Sale elimination.'},status=status.HTTP_400_BAD_REQUEST)