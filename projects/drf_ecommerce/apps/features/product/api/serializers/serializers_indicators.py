# py
# django
# drf
from rest_framework import serializers
# third
# own
from apps.features.product.models import Indicators
from apps.features.product.api.serializers.serializers_categories_product import CategoriesProductViewSerializer

class IndicatorsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicators
        fields = '__all__'
    
    category = CategoriesProductViewSerializer()

class IndicatorsActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicators
        exclude = ('id','is_active','created_at','updated_at','deleted_at')
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'descount_value': instance.descount_value,
            'category': {
                'id': instance.category.id,
                'description': instance.description
            },
        }