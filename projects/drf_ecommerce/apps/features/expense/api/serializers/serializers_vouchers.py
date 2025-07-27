# py
# django
# drf
from rest_framework import serializers
# third
# own
from apps.features.expense.models import Vouchers

class VouchersViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vouchers
        fields = '__all__'

class VouchersActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vouchers
        exclude = ('id','is_active','created_at','updated_at','deleted_at')