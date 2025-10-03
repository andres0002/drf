# py
# django
# drf
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
# thrid
# own
from apps.core.api.viewsets.viewsets import (
    PublicGeneralViewSets,
    PrivateGeneralModelViewSets
)
from apps.features.expense.api.serializers.serializers import (
    ExpenseCategoriesViewSerializer,
    ExpenseCategoriesActionsSerializer
)

class PublicExpenseCategoriesViewSets(PublicGeneralViewSets):
    serializer_class = ExpenseCategoriesActionsSerializer
    serializer_view_class = ExpenseCategoriesViewSerializer
    
    def list(self, request, *args, **kwargs):
        expense_categories = self.get_queryset()
        expense_categories_serializer = self.get_serializer(expense_categories, many = True)
        return Response(expense_categories_serializer.data,status=status.HTTP_200_OK)

class PrivateExpenseCategoriesModelViewSets(PrivateGeneralModelViewSets):
    serializer_class = ExpenseCategoriesActionsSerializer
    serializer_view_class = ExpenseCategoriesViewSerializer

    # elimination logical. -> para elimination direct se comenta el method destroy().
    def destroy(self, request, *args, **kwargs):
        expense_category = self.get_object()
        if expense_category:
            expense_category.is_active = False
            expense_category.save()
            return Response({'message':'Successfully Expense Category elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful Expense Category elimination.'},status=status.HTTP_400_BAD_REQUEST)