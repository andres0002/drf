# py
# django
# from django.urls import path
# drf
from rest_framework.routers import DefaultRouter # type: ignore
# third
# own
from apps.features.expense.api.viewsets.viewsets import (
    PublicSuppliersViewSets,
    PrivateSuppliersModelViewSets,
    PublicVouchersViewSets,
    PrivateVouchersModelViewSets,
    PublicExpenseCategoriesViewSets,
    PrivateExpenseCategoriesModelViewSets,
    PublicExpensesViewSets,
    PrivateExpensesModelViewSets,
    PublicMermasViewSets,
    PrivateMermasModelViewSets
)

router = DefaultRouter()

# suppliers.
router.register(r'public_suppliers', PublicSuppliersViewSets, basename='public_suppliers')
router.register(r'private_suppliers', PrivateSuppliersModelViewSets, basename='private_suppliers')
# vouchers.
router.register(r'public_vouchers', PublicVouchersViewSets, basename='public_vouchers')
router.register(r'private_vouchers', PrivateVouchersModelViewSets, basename='private_vouchers')
# expense categories.
router.register(r'public_expense_categories', PublicExpenseCategoriesViewSets, basename='public_expense_categories')
router.register(r'private_expense_categories', PrivateExpenseCategoriesModelViewSets, basename='private_expense_categories')
# expenses.
router.register(r'public_expenses', PublicExpensesViewSets, basename='public_expenses')
router.register(r'private_expenses', PrivateExpensesModelViewSets, basename='private_expenses')
# mermas.
router.register(r'public_mermas', PublicMermasViewSets, basename='public_mermas')
router.register(r'private_mermas', PrivateMermasModelViewSets, basename='private_mermas')

# instance urlpatterns.
urlpatterns = []
# populate instance.
urlpatterns += router.urls

# print('URLPATTERNS:', urlpatterns)
# for url in urlpatterns:
#     print(url)