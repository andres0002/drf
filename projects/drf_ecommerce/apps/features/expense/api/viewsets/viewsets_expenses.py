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
    ExpensesViewSerializer,
    ExpensesActionsSerializer
)

class PublicExpensesViewSets(PublicGeneralViewSets):
    serializer_class = ExpensesActionsSerializer
    serializer_view_class = ExpensesViewSerializer
    
    def list(self, request, *args, **kwargs):
        expenses = self.get_queryset()
        expenses_serializer = self.get_serializer(expenses, many = True)
        return Response(expenses_serializer.data,status=status.HTTP_200_OK)

class PrivateExpensesModelViewSets(PrivateGeneralModelViewSets):
    serializer_class = ExpensesActionsSerializer
    serializer_view_class = ExpensesViewSerializer

    # elimination logical. -> para elimination direct se comenta el method destroy().
    def destroy(self, request, *args, **kwargs):
        expense = self.get_object()
        if expense:
            expense.is_active = False
            expense.save()
            return Response({'message':'Successfully Expense elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful Expense elimination.'},status=status.HTTP_400_BAD_REQUEST)