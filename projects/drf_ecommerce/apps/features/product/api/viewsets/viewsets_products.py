# py
# django
# drf
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# third
# own
from apps.core.api.viewsets.viewsets import (
    PublicGeneralViewSets,
    PrivateGeneralModelViewSets
)
from apps.features.product.api.serializers.serializers import (
    ProductsViewSerializer,
    ProductsActionsSerializer
)

class PublicProductsViewSets(PublicGeneralViewSets):
    serializer_class = ProductsActionsSerializer
    serializer_view_class = ProductsViewSerializer
    
    def list(self, request, *args, **kwargs):
        products = self.get_queryset()
        products_serializer = self.get_serializer(products, many = True)
        return Response(products_serializer.data,status=status.HTTP_200_OK)

class PrivateProductsModelViewSets(PrivateGeneralModelViewSets):
    serializer_view_class = ProductsViewSerializer
    serializer_class = ProductsActionsSerializer
    
    # elimination logical. -> para elimination direct se comenta el method delete().
    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product:
            product.is_active = False
            product.save()
            return Response({'message':'Successfully Product elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful Product elimination.'},status=status.HTTP_400_BAD_REQUEST)