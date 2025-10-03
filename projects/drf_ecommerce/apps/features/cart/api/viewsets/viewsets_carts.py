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
from apps.features.cart.api.serializers.serializers import (
    CartsViewSerializer,
    CartsActionsSerializer
)

class PublicCartsViewSets(PublicGeneralViewSets):
    serializer_class = CartsActionsSerializer
    serializer_view_class = CartsViewSerializer
    
    def list(self, request, *args, **kwargs):
        carts = self.get_queryset()
        carts_serializer = self.get_serializer(carts, many = True)
        return Response(carts_serializer.data,status=status.HTTP_200_OK)

class PrivateCartsModelViewSets(PrivateGeneralModelViewSets):
    serializer_class = CartsActionsSerializer
    serializer_view_class = CartsViewSerializer

    # elimination logical. -> para elimination direct se comenta el method destroy().
    def destroy(self, request, *args, **kwargs):
        cart = self.get_object()
        if cart:
            cart.is_active = False
            cart.save()
            return Response({'message':'Successfully Cart elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful Cart elimination.'},status=status.HTTP_400_BAD_REQUEST)