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
    CartItemsViewSerializer,
    CartItemsActionsSerializer
)

class PublicCartItemsViewSets(PublicGeneralViewSets):
    serializer_class = CartItemsActionsSerializer
    serializer_view_class = CartItemsViewSerializer
    
    def list(self, request, *args, **kwargs):
        cart_items = self.get_queryset()
        cart_items_serializer = self.get_serializer(cart_items, many = True)
        return Response(cart_items_serializer.data,status=status.HTTP_200_OK)

class PrivateCartItemsModelViewSets(PrivateGeneralModelViewSets):
    serializer_class = CartItemsActionsSerializer
    serializer_view_class = CartItemsViewSerializer

    # elimination logical. -> para elimination direct se comenta el method destroy().
    def destroy(self, request, *args, **kwargs):
        cart_item = self.get_object()
        if cart_item:
            cart_item.is_active = False
            cart_item.save()
            return Response({'message':'Successfully Cart Item elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful Cart Item elimination.'},status=status.HTTP_400_BAD_REQUEST)