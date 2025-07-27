# py
# django
# drf
from rest_framework import serializers
# third
# own
from apps.features.product.models import CategoriesProduct

class CategoriesProductViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriesProduct
        fields = '__all__'

class CategoriesProductActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriesProduct
        exclude = ('id','is_active','created_at','updated_at','deleted_at')