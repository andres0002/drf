# py
# django
# drf
from rest_framework import serializers
# third
# own
from apps.features.expense.models import Suppliers

class SuppliersViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = '__all__'

class SuppliersActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        exclude = ('id','is_active','created_at','updated_at','deleted_at')