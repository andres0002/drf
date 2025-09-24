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
from apps.features.sale.api.serializers.serializers import (
    CustomersViewSerializer,
    CustomersActionsSerializer
)

class PublicCustomersViewSets(PublicGeneralViewSets):
    serializer_class = CustomersActionsSerializer
    serializer_view_class = CustomersViewSerializer
    
    def list(self, request, *args, **kwargs):
        customers = self.get_queryset()
        customers_serializer = self.get_serializer(customers, many = True)
        return Response(customers_serializer.data,status=status.HTTP_200_OK)

class PrivateCustomersModelViewSets(PrivateGeneralModelViewSets):
    serializer_view_class = CustomersViewSerializer
    serializer_class = CustomersActionsSerializer

    # elimination logical. -> para elimination direct se comenta el method destroy().
    def destroy(self, request, *args, **kwargs):
        customer = self.get_object()
        if customer:
            customer.is_active = False
            customer.save()
            return Response({'message':'Successfully Customer elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful Customer elimination.'},status=status.HTTP_400_BAD_REQUEST)