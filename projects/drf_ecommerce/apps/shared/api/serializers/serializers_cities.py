# py
# django
# drf
from rest_framework import serializers # type: ignore
# third
# own
from apps.shared.models import Cities

class CitiesViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        fields = '__all__'

class CitiesActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cities
        exclude = ('id','is_active','created_at','updated_at','deleted_at')