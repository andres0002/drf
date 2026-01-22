# py
# django
from django.contrib.auth.models import Group
# drf
from rest_framework import serializers
# third
# own
from apps.features.user.api.serializers.serializers_permissions import (
    UserPermissionsViewSerializer
)

class GroupsViewSerializer(serializers.ModelSerializer):
    permissions = UserPermissionsViewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']

class GroupsActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']