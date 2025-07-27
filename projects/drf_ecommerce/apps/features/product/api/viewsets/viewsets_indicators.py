# py
# django
# drf
from rest_framework.response import Response
from rest_framework import status
# thrid
# own
from apps.core.api.viewsets.viewsets import (
    PublicGeneralViewSets,
    PrivateGeneralModelViewSets
)
from apps.features.product.api.serializers.serializers import (
    IndicatorsViewSerializer,
    IndicatorsActionsSerializer
)

class PublicIndicatorsViewSets(PublicGeneralViewSets):
    serializer_class = IndicatorsActionsSerializer
    serializer_view_class = IndicatorsViewSerializer
    
    def list(self, request, *args, **kwargs):
        indicators = self.get_queryset()
        indicators_serializer = self.get_serializer(indicators, many = True)
        return Response(indicators_serializer.data,status=status.HTTP_200_OK)

class PrivateIndicatorsModelViewSets(PrivateGeneralModelViewSets):
    serializer_view_class = IndicatorsViewSerializer
    serializer_class = IndicatorsActionsSerializer

    # elimination logical. -> para elimination direct se comenta el method delete().
    def destroy(self, request, *args, **kwargs):
        indicator = self.get_object()
        if indicator:
            indicator.is_active = False
            indicator.save()
            return Response({'message':'Successfully Category Product elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful Category Product elimination.'},status=status.HTTP_400_BAD_REQUEST)