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
    ProductCategoriesViewSerializer,
    ProductCategoriesActionsSerializer
)

class PublicProductCategoriesViewSets(PublicGeneralViewSets):
    serializer_class = ProductCategoriesActionsSerializer
    serializer_view_class = ProductCategoriesViewSerializer
    
    def list(self, request, *args, **kwargs):
        product_categories = self.get_queryset()
        product_categories_serializer = self.get_serializer(product_categories, many = True)
        return Response(product_categories_serializer.data,status=status.HTTP_200_OK)

class PrivateProductCategoriesModelViewSets(PrivateGeneralModelViewSets):
    serializer_view_class = ProductCategoriesViewSerializer
    serializer_class = ProductCategoriesActionsSerializer

    # elimination logical. -> para elimination direct se comenta el method destroy().
    def destroy(self, request, *args, **kwargs):
        product_category = self.get_object()
        if product_category:
            product_category.is_active = False
            product_category.save()
            return Response({'message':'Successfully Product Category elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful Product Category elimination.'},status=status.HTTP_400_BAD_REQUEST)