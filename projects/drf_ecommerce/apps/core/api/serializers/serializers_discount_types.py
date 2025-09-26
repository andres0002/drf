# py
# django
# drf
from rest_framework import serializers # type: ignore
# third
# own
from apps.core.models import DiscountTypes

class DiscountTypesViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountTypes
        fields = '__all__'

class DiscountTypesActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountTypes
        exclude = ('id','is_active','created_at','updated_at','deleted_at')