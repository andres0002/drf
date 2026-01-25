# py
# django
# drf
from rest_framework import serializers # type: ignore
# third
# own
from apps.features.user.models import AccessLogs

class AccessLogsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessLogs
        fields = '__all__'

class AccessLogsActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessLogs
        exclude = ('id','is_active','created_at','updated_at','deleted_at')