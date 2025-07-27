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
    MermasViewSerializer,
    MermasActionsSerializer
)

class PublicMermasViewSets(PublicGeneralViewSets):
    serializer_class = MermasActionsSerializer
    serializer_view_class = MermasViewSerializer
    
    def list(self, request, *args, **kwargs):
        mermas = self.get_queryset()
        mermas_serializer = self.get_serializer(mermas, many = True)
        return Response(mermas_serializer.data,status=status.HTTP_200_OK)

class PrivateMermasModelViewSets(PrivateGeneralModelViewSets):
    serializer_class = MermasActionsSerializer
    serializer_view_class = MermasViewSerializer

    # elimination logical. -> para elimination direct se comenta el method destroy().
    def destroy(self, request, *args, **kwargs):
        merma = self.get_object()
        if merma:
            merma.is_active = False
            merma.save()
            return Response({'message':'Successfully Merma elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful Merma elimination.'},status=status.HTTP_400_BAD_REQUEST)