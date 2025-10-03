# py
# django
# drf
from rest_framework import serializers # type: ignore
# third
# own
from apps.core.models import MovementTypes

class MovementTypesViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovementTypes
        fields = '__all__'

class MovementTypesActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovementTypes
        exclude = ('id','is_active','created_at','updated_at','deleted_at')