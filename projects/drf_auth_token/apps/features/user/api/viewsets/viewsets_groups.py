# py
# django
# drf
from rest_framework.response import Response
from rest_framework import status
# third
# own
from apps.core.api.viewsets.viewsets import (
    PublicGeneralViewSets,
    PrivateGeneralModelViewSets
)
from apps.core.mixins import BulkDeleteLogicalAndDirectDisabledMixin
from apps.features.user.api.serializers.serializers import (
    GroupsViewSerializer,
    GroupsActionsSerializer
)

# Create your views here.

class PublicGroupsViewSets(PublicGeneralViewSets):
    serializer_class = GroupsActionsSerializer
    serializer_view_class = GroupsViewSerializer
    
    def get_queryset(self):
        model = self.get_serializer_class().Meta.model
        return model.objects.all()
    
    def list(self, request, *args, **kwargs):
        groups = self.get_queryset()
        groups_serializer = self.get_serializer(groups, many = True)
        return Response(groups_serializer.data,status=status.HTTP_200_OK)

class PrivateGroupsModelViewSets(BulkDeleteLogicalAndDirectDisabledMixin, PrivateGeneralModelViewSets):
    serializer_view_class = GroupsViewSerializer
    serializer_class = GroupsActionsSerializer
    
    def get_queryset(self):
        model = self.get_serializer().Meta.model
        return model.objects.all()