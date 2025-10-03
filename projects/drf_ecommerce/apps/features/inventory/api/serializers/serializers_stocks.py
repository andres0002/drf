# py
# django
# drf
from rest_framework import serializers # type: ignore
# third
# own
from apps.features.inventory.models import Stocks
from apps.features.product.api.serializers.serializers import (
    ProductsViewSerializer
)

class StocksViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stocks
        fields = '__all__'
    
    product = ProductsViewSerializer()

class StocksActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stocks
        exclude = ('id','is_active','created_at','updated_at','deleted_at')