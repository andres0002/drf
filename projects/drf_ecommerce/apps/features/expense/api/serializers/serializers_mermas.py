# py
# django
# drf
from rest_framework import serializers
# third
# own
from apps.features.expense.models import Mermas

class MermasViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mermas
        fields = '__all__'

class MermasActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mermas
        exclude = ('id','is_active','created_at','updated_at','deleted_at')