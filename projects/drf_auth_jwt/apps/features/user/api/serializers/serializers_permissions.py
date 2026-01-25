# py
# django
from django.contrib.auth.models import Permission
# drf
from rest_framework import serializers
# third
# own

class UserPermissionsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'codename', 'name']

class UserPermissionsActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'codename', 'name']