# py
# django
# drf
from rest_framework import serializers # type: ignore
# third
# own
from apps.features.sale.models import Sales

class SalesViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'

class SalesActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        exclude = ('id','is_active','created_at','updated_at','deleted_at')