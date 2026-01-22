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
from apps.core.api.serializers.serializers import (
    DocumentTypesViewSerializer,
    DocumentTypesActionsSerializer
)

class PublicDocumentTypesViewSets(PublicGeneralViewSets):
    serializer_class = DocumentTypesActionsSerializer
    serializer_view_class = DocumentTypesViewSerializer
    
    def list(self, request, *args, **kwargs):
        document_types = self.get_queryset()
        document_types_serializer = self.get_serializer(document_types, many = True)
        return Response(document_types_serializer.data,status=status.HTTP_200_OK)

class PrivateDocumentTypesModelViewSets(PrivateGeneralModelViewSets):
    serializer_class = DocumentTypesActionsSerializer
    serializer_view_class = DocumentTypesViewSerializer

    # elimination logical. -> para elimination direct se comenta el method destroy().
    def destroy(self, request, *args, **kwargs):
        document_type = self.get_object()
        if document_type:
            document_type.is_active = False
            document_type.save()
            return Response({'message':'Successfully Document Type elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful Document Type elimination.'},status=status.HTTP_400_BAD_REQUEST)