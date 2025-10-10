# py
# django
# drf
from rest_framework import serializers # type: ignore
# third
# own
from apps.features.inventory.models import WarehouseTransfers

class WarehouseTransfersViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseTransfers
        fields = '__all__'
    
    # product = ProductsViewSerializer()

class WarehouseTransfersActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseTransfers
        exclude = ('id','is_active','created_at','updated_at','deleted_at')