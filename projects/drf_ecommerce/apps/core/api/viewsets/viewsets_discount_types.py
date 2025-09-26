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
    DiscountTypesViewSerializer,
    DiscountTypesActionsSerializer
)

class PublicDiscountTypesViewSets(PublicGeneralViewSets):
    serializer_class = DiscountTypesActionsSerializer
    serializer_view_class = DiscountTypesViewSerializer
    
    def list(self, request, *args, **kwargs):
        discount_types = self.get_queryset()
        discount_types_serializer = self.get_serializer(discount_types, many = True)
        return Response(discount_types_serializer.data,status=status.HTTP_200_OK)

class PrivateDiscountTypesModelViewSets(PrivateGeneralModelViewSets):
    serializer_class = DiscountTypesActionsSerializer
    serializer_view_class = DiscountTypesViewSerializer

    # elimination logical. -> para elimination direct se comenta el method destroy().
    def destroy(self, request, *args, **kwargs):
        discount_type = self.get_object()
        if discount_type:
            discount_type.is_active = False
            discount_type.save()
            return Response({'message':'Successfully Discount Type elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful Discount Type elimination.'},status=status.HTTP_400_BAD_REQUEST)