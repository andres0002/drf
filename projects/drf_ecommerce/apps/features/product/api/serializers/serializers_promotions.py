# py
# django
# drf
from rest_framework import serializers # type: ignore
# third
# own
from apps.features.product.models import Promotions
# from apps.features.product.api.serializers.serializers_categories_product import CategoriesProductViewSerializer

class PromotionsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotions
        fields = '__all__'
    
    # category = CategoriesProductViewSerializer()

class PromotionsActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotions
        exclude = ('id','is_active','created_at','updated_at','deleted_at')
    
    # def to_representation(self, instance):
    #     return {
    #         'id': instance.id,
    #         'discount_value': instance.discount_value,
    #         'category': {
    #             'id': instance.category.id,
    #             'description': instance.description
    #         },
    #     }