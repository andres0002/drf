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
from apps.features.product.api.serializers.serializers import  (
    MeasureUnitsViewSerializer,
    MeasureUnitsActionsSerializer
)

class PublicMeasureUnitsViewSets(PublicGeneralViewSets):
    serializer_class = MeasureUnitsActionsSerializer
    serializer_view_class = MeasureUnitsViewSerializer
    
    def list(self, request, *args, **kwargs):
        measure_units = self.get_queryset()
        measure_units_serializer = self.get_serializer(measure_units, many = True)
        return Response(measure_units_serializer.data,status=status.HTTP_200_OK)

class PrivateMeasureUnitsModelViewSets(PrivateGeneralModelViewSets):
    serializer_view_class = MeasureUnitsViewSerializer
    serializer_class = MeasureUnitsActionsSerializer

    # elimination logical. -> para elimination direct se comenta el method destroy().
    def destroy(self, request, *args, **kwargs):
        measure_unit = self.get_object()
        if measure_unit:
            measure_unit.is_active = False
            measure_unit.save()
            return Response({'message':'Successfully Measure Unit elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful Measure Unit elimination.'},status=status.HTTP_400_BAD_REQUEST)