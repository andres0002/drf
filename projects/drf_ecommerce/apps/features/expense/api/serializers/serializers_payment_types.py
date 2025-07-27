# py
# django
# drf
from rest_framework import serializers
# third
# own
from apps.features.expense.models import PaymentTypes

class PaymentTypesViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTypes
        fields = '__all__'

class PaymentTypesActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTypes
        exclude = ('id','is_active','created_at','updated_at','deleted_at')