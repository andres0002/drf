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
from apps.features.expense.api.serializers.serializers import (
    PaymentTypesViewSerializer,
    PaymentTypesActionsSerializer
)

class PublicPaymentTypesViewSets(PublicGeneralViewSets):
    serializer_class = PaymentTypesActionsSerializer
    serializer_view_class = PaymentTypesViewSerializer
    
    def list(self, request, *args, **kwargs):
        payment_types = self.get_queryset()
        payment_types_serializer = self.get_serializer(payment_types, many = True)
        return Response(payment_types_serializer.data,status=status.HTTP_200_OK)

class PrivatePaymentTypesModelViewSets(PrivateGeneralModelViewSets):
    serializer_class = PaymentTypesActionsSerializer
    serializer_view_class = PaymentTypesViewSerializer

    # elimination logical. -> para elimination direct se comenta el method destroy().
    def destroy(self, request, *args, **kwargs):
        payment_type = self.get_object()
        if payment_type:
            payment_type.is_active = False
            payment_type.save()
            return Response({'message':'Successfully Payment Type elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful Payment Type elimination.'},status=status.HTTP_400_BAD_REQUEST)