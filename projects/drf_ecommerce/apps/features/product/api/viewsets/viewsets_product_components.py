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
    ProductComponentsViewSerializer,
    ProductComponentsActionsSerializer
)

class PublicProductComponentsViewSets(PublicGeneralViewSets):
    serializer_class = ProductComponentsActionsSerializer
    serializer_view_class = ProductComponentsViewSerializer
    
    def list(self, request, *args, **kwargs):
        product_components = self.get_queryset()
        product_components_serializer = self.get_serializer(product_components, many = True)
        return Response(product_components_serializer.data,status=status.HTTP_200_OK)

class PrivateProductComponentsModelViewSets(PrivateGeneralModelViewSets):
    serializer_view_class = ProductComponentsViewSerializer
    serializer_class = ProductComponentsActionsSerializer

    # elimination logical. -> para elimination direct se comenta el method destroy().
    def destroy(self, request, *args, **kwargs):
        product_component = self.get_object()
        if product_component:
            product_component.is_active = False
            product_component.save()
            return Response({'message':'Successfully Product Component elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful Product Component elimination.'},status=status.HTTP_400_BAD_REQUEST)