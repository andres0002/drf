# py
# django
# drf
from rest_framework import serializers # type: ignore
# third
# own
from apps.features.expense.models import ExpenseCategories

class ExpenseCategoriesViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategories
        fields = '__all__'

class ExpenseCategoriesActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategories
        exclude = ('id','is_active','created_at','updated_at','deleted_at')