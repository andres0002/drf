# py
# django
# drf
from rest_framework import serializers # type: ignore
# third
# own
from apps.features.cart.models import Carts
from apps.features.user.api.serializers.serializers import (
    UsersViewSerializer
)

class CartsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carts
        fields = '__all__'
    
    user = UsersViewSerializer()

class CartsActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carts
        exclude = ('id','is_active','created_at','updated_at','deleted_at')