# py
# django
# drf
from rest_framework import serializers
# third
# own
from apps.features.product.models import MeasureUnits

class MeasureUnitsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasureUnits
        fields = '__all__'

class MeasureUnitsActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasureUnits
        exclude = ('id','is_active','created_at','updated_at','deleted_at')