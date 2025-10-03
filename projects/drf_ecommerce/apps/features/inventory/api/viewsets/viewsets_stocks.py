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
    StocksViewSerializer,
    StocksActionsSerializer
)

class PublicStocksViewSets(PublicGeneralViewSets):
    serializer_class = StocksActionsSerializer
    serializer_view_class = StocksViewSerializer
    
    def list(self, request, *args, **kwargs):
        stocks = self.get_queryset()
        stocks_serializer = self.get_serializer(stocks, many = True)
        return Response(stocks_serializer.data,status=status.HTTP_200_OK)

class PrivateStocksModelViewSets(PrivateGeneralModelViewSets):
    serializer_class = StocksActionsSerializer
    serializer_view_class = StocksViewSerializer

    # elimination logical. -> para elimination direct se comenta el method destroy().
    def destroy(self, request, *args, **kwargs):
        stock = self.get_object()
        if stock:
            stock.is_active = False
            stock.save()
            return Response({'message':'Successfully Stock elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful Stock elimination.'},status=status.HTTP_400_BAD_REQUEST)