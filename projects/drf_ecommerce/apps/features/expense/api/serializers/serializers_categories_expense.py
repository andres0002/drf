# py
# django
# drf
from rest_framework import serializers
# third
# own
from apps.features.expense.models import CategoriesExpense

class CategoriesExpenseViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriesExpense
        fields = '__all__'

class CategoriesExpenseActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriesExpense
        exclude = ('id','is_active','created_at','updated_at','deleted_at')