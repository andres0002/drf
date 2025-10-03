# py
# django
# drf
from rest_framework import serializers # type: ignore
# third
# own
from apps.features.cart.models import CartItems
from apps.features.cart.api.serializers.serializers import (
    CartsViewSerializer
)
from apps.features.product.api.serializers.serializers import (
    ProductsViewSerializer
)

class CartItemsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = '__all__'
    
    cart = CartsViewSerializer()
    product = ProductsViewSerializer()

class CartItemsActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        exclude = ('id','is_active','created_at','updated_at','deleted_at')