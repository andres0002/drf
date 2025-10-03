# py
# django
# drf
from rest_framework import serializers # type: ignore
# third
# own
from apps.features.inventory.models import InventoryMovements
from apps.core.api.serializers.serializers import (
    MovementTypesViewSerializer
)
from apps.features.product.api.serializers.serializers import (
    ProductsViewSerializer
)
from apps.features.sale.api.serializers.serializers import (
    SalesViewSerializer
)
from apps.features.expense.api.serializers.serializers import (
    ExpensesViewSerializer
)

class InventoryMovementsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryMovements
        fields = '__all__'
    
    product = ProductsViewSerializer()
    movement_type = MovementTypesViewSerializer()
    reference_sale = SalesViewSerializer()
    reference_expense = ExpensesViewSerializer()

class InventoryMovementsActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryMovements
        exclude = ('id','is_active','created_at','updated_at','deleted_at')