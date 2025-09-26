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
from apps.features.product.api.serializers.serializers import (
    PromotionsViewSerializer,
    PromotionsActionsSerializer
)

class PublicPromotionsViewSets(PublicGeneralViewSets):
    serializer_class = PromotionsActionsSerializer
    serializer_view_class = PromotionsViewSerializer
    
    def list(self, request, *args, **kwargs):
        promotions = self.get_queryset()
        promotions_serializer = self.get_serializer(promotions, many = True)
        return Response(promotions_serializer.data,status=status.HTTP_200_OK)

class PrivatePromotionsModelViewSets(PrivateGeneralModelViewSets):
    serializer_view_class = PromotionsViewSerializer
    serializer_class = PromotionsActionsSerializer

    # elimination logical. -> para elimination direct se comenta el method delete().
    def destroy(self, request, *args, **kwargs):
        promotion = self.get_object()
        if promotion:
            promotion.is_active = False
            promotion.save()
            return Response({'message':'Successfully Promotion elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful Promotion elimination.'},status=status.HTTP_400_BAD_REQUEST)