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
from apps.features.user.api.serializers.serializers import (
    FingerprintsViewSerializer,
    FingerprintsActionsSerializer
)

class PublicFingerprintsViewSets(PublicGeneralViewSets):
    serializer_class = FingerprintsActionsSerializer
    serializer_view_class = FingerprintsViewSerializer
    
    def list(self, request, *args, **kwargs):
        fingerprints = self.get_queryset()
        fingerprints_serializer = self.get_serializer(fingerprints, many = True)
        return Response(fingerprints_serializer.data,status=status.HTTP_200_OK)

class PrivateFingerprintsModelViewSets(PrivateGeneralModelViewSets):
    serializer_class = FingerprintsActionsSerializer
    serializer_view_class = FingerprintsViewSerializer

    # elimination logical. -> para elimination direct se comenta el method destroy().
    def destroy(self, request, *args, **kwargs):
        fingerprint = self.get_object()
        if fingerprint:
            fingerprint.is_active = False
            fingerprint.save()
            return Response({'message':'Successfully Fingerprint elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful Fingerprint elimination.'},status=status.HTTP_400_BAD_REQUEST)