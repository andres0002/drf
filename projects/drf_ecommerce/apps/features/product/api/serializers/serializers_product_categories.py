# py
# django
# drf
from rest_framework import serializers
# third
# own
from apps.features.product.models import ProductCategories

class ProductCategoriesViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategories
        fields = '__all__'

class ProductCategoriesActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategories
        exclude = ('id','is_active','created_at','updated_at','deleted_at')