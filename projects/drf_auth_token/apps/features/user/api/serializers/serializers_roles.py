# py
# django
# drf
from rest_framework import serializers # type: ignore
# third
# own
from apps.features.user.models import Roles

class RolesViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'

class RolesActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        exclude = ('id','is_active','created_at','updated_at','deleted_at')