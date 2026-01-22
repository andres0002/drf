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
    CountriesViewSerializer,
    CountriesActionsSerializer
)

class PublicCountriesViewSets(PublicGeneralViewSets):
    serializer_class = CountriesActionsSerializer
    serializer_view_class = CountriesViewSerializer
    
    def list(self, request, *args, **kwargs):
        countries = self.get_queryset()
        countries_serializer = self.get_serializer(countries, many = True)
        return Response(countries_serializer.data,status=status.HTTP_200_OK)

class PrivateCountriesModelViewSets(PrivateGeneralModelViewSets):
    serializer_class = CountriesActionsSerializer
    serializer_view_class = CountriesViewSerializer

    # elimination logical. -> para elimination direct se comenta el method destroy().
    def destroy(self, request, *args, **kwargs):
        country = self.get_object()
        if country:
            country.is_active = False
            country.save()
            return Response({'message':'Successfully Country elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful Country elimination.'},status=status.HTTP_400_BAD_REQUEST)