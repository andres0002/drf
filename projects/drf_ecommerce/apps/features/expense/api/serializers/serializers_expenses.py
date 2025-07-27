# py
# django
# drf
from rest_framework import serializers
# third
# own
from apps.features.expense.models import Expenses
from apps.features.expense.api.serializers.serializers import (
    SuppliersViewSerializer,
    VouchersViewSerializer,
    PaymentTypesViewSerializer
)
from apps.features.user.api.serializers.serializers import (
    UsersViewSerializer
)
from apps.features.product.api.serializers.serializers import (
    ProductsViewSerializer
)

class ExpensesViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = '__all__'
    
    supplier = SuppliersViewSerializer()
    voucher = VouchersViewSerializer()
    payment_type = PaymentTypesViewSerializer()
    user = UsersViewSerializer()
    product = ProductsViewSerializer()

class ExpensesActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        exclude = ('id','is_active','created_at','updated_at','deleted_at')