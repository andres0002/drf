# py
# django
# drf
from rest_framework import serializers # type: ignore
# third
# own
from apps.features.inventory.models import Warehouses

class WarehousesViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouses
        fields = '__all__'
    
    # product = ProductsViewSerializer()

class WarehousesActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouses
        exclude = ('id','is_active','created_at','updated_at','deleted_at')