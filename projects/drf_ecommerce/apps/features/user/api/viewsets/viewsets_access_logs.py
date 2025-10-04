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
    AccessLogsViewSerializer,
    AccessLogsActionsSerializer
)

class PublicAccessLogsViewSets(PublicGeneralViewSets):
    serializer_class = AccessLogsActionsSerializer
    serializer_view_class = AccessLogsViewSerializer
    
    def list(self, request, *args, **kwargs):
        access_logs = self.get_queryset()
        access_logs_serializer = self.get_serializer(access_logs, many = True)
        return Response(access_logs_serializer.data,status=status.HTTP_200_OK)

class PrivateAccessLogsModelViewSets(PrivateGeneralModelViewSets):
    serializer_class = AccessLogsActionsSerializer
    serializer_view_class = AccessLogsViewSerializer

    # elimination logical. -> para elimination direct se comenta el method destroy().
    def destroy(self, request, *args, **kwargs):
        access_log = self.get_object()
        if access_log:
            access_log.is_active = False
            access_log.save()
            return Response({'message':'Successfully Access Log elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful Access Log elimination.'},status=status.HTTP_400_BAD_REQUEST)