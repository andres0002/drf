# py
# django
# drf
from rest_framework import serializers # type: ignore
# third
# own
from apps.core.models import DocumentTypes

class DocumentTypesViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentTypes
        fields = '__all__'

class DocumentTypesActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentTypes
        exclude = ('id','is_active','created_at','updated_at','deleted_at')