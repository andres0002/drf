# py
# django
# drf
from rest_framework import serializers # type: ignore
# third
# own
from apps.features.sale.models import Customers

class CustomersViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = '__all__'

class CustomersActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        exclude = ('id','is_active','created_at','updated_at','deleted_at')