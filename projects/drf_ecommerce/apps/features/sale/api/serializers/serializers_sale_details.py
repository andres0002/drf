# py
# django
# drf
from rest_framework import serializers # type: ignore
# third
# own
from apps.features.sale.models import SaleDetails

class SaleDetailsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleDetails
        fields = '__all__'

class SaleDetailsActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleDetails
        exclude = ('id','is_active','created_at','updated_at','deleted_at')