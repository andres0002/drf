# py
# django
# drf
from rest_framework import serializers # type: ignore
# third
# own
from apps.features.product.models import ProductComponents
from apps.core.api.serializers.serializers import MeasureUnitsViewSerializer
from apps.features.product.api.serializers.serializers import ProductsViewSerializer

class ProductComponentsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComponents
        fields = '__all__'
    
    product = ProductsViewSerializer()
    subproduct = ProductsViewSerializer()
    measure_unit = MeasureUnitsViewSerializer()

class ProductComponentsActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComponents
        exclude = ('id','is_active','created_at','updated_at','deleted_at')