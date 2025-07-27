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
    VouchersViewSerializer,
    VouchersActionsSerializer
)

class PublicVouchersViewSets(PublicGeneralViewSets):
    serializer_class = VouchersActionsSerializer
    serializer_view_class = VouchersViewSerializer
    
    def list(self, request, *args, **kwargs):
        vouchers = self.get_queryset()
        vouchers_serializer = self.get_serializer(vouchers, many = True)
        return Response(vouchers_serializer.data,status=status.HTTP_200_OK)

class PrivateVouchersModelViewSets(PrivateGeneralModelViewSets):
    serializer_class = VouchersActionsSerializer
    serializer_view_class = VouchersViewSerializer

    # elimination logical. -> para elimination direct se comenta el method destroy().
    def destroy(self, request, *args, **kwargs):
        voucher = self.get_object()
        if voucher:
            voucher.is_active = False
            voucher.save()
            return Response({'message':'Successfully Voucher elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful Voucher elimination.'},status=status.HTTP_400_BAD_REQUEST)