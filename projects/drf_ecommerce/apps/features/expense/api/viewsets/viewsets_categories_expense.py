# py
# django
# drf
from rest_framework.response import Response
from rest_framework import status
# thrid
# own
from apps.core.api.viewsets.viewsets import (
    PublicGeneralViewSets,
    PrivateGeneralModelViewSets
)
from apps.features.expense.api.serializers.serializers import (
    CategoriesExpenseViewSerializer,
    CategoriesExpenseActionsSerializer
)

class PublicCategoriesExpenseViewSets(PublicGeneralViewSets):
    serializer_class = CategoriesExpenseActionsSerializer
    serializer_view_class = CategoriesExpenseViewSerializer
    
    def list(self, request, *args, **kwargs):
        categories_expense = self.get_queryset()
        categories_expense_serializer = self.get_serializer(categories_expense, many = True)
        return Response(categories_expense_serializer.data,status=status.HTTP_200_OK)

class PrivateCategoriesExpenseModelViewSets(PrivateGeneralModelViewSets):
    serializer_class = CategoriesExpenseActionsSerializer
    serializer_view_class = CategoriesExpenseViewSerializer

    # elimination logical. -> para elimination direct se comenta el method destroy().
    def destroy(self, request, *args, **kwargs):
        category_expense = self.get_object()
        if category_expense:
            category_expense.is_active = False
            category_expense.save()
            return Response({'message':'Successfully Category Expense elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful Category Expense elimination.'},status=status.HTTP_400_BAD_REQUEST)