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
from apps.shared.api.serializers.serializers import (
    CitiesViewSerializer,
    CitiesActionsSerializer
)

class PublicCitiesViewSets(PublicGeneralViewSets):
    serializer_class = CitiesActionsSerializer
    serializer_view_class = CitiesViewSerializer
    
    def list(self, request, *args, **kwargs):
        cities = self.get_queryset()
        cities_serializer = self.get_serializer(cities, many = True)
        return Response(cities_serializer.data,status=status.HTTP_200_OK)

class PrivateCitiesModelViewSets(PrivateGeneralModelViewSets):
    serializer_class = CitiesActionsSerializer
    serializer_view_class = CitiesViewSerializer

    # elimination logical. -> para elimination direct se comenta el method destroy().
    def destroy(self, request, *args, **kwargs):
        city = self.get_object()
        if city:
            city.is_active = False
            city.save()
            return Response({'message':'Successfully City elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful City elimination.'},status=status.HTTP_400_BAD_REQUEST)