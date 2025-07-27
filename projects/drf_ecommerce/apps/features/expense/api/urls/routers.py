# py
# django
# from django.urls import path
# drf
from rest_framework.routers import DefaultRouter
# third
# own
from apps.features.expense.api.viewsets.viewsets import (
    PublicSuppliersViewSets,
    PrivateSuppliersModelViewSets,
    PublicPaymentTypesViewSets,
    PrivatePaymentTypesModelViewSets,
    PublicVouchersViewSets,
    PrivateVouchersModelViewSets,
    PublicCategoriesExpenseViewSets,
    PrivateCategoriesExpenseModelViewSets,
    PublicExpensesViewSets,
    PrivateExpensesModelViewSets,
    PublicMermasViewSets,
    PrivateMermasModelViewSets
)

router = DefaultRouter()

# suppliers.
router.register(r'public_suppliers', PublicSuppliersViewSets, basename='public_suppliers')
router.register(r'private_suppliers', PrivateSuppliersModelViewSets, basename='private_suppliers')
# payment types.
router.register(r'public_payment_types', PublicPaymentTypesViewSets, basename='public_payment_types')
router.register(r'private_payment_types', PrivatePaymentTypesModelViewSets, basename='private_payment_types')
# vouchers.
router.register(r'public_vouchers', PublicVouchersViewSets, basename='public_vouchers')
router.register(r'private_vouchers', PrivateVouchersModelViewSets, basename='private_vouchers')
# categories expense.
router.register(r'public_categories_expense', PublicCategoriesExpenseViewSets, basename='public_categories_expense')
router.register(r'private_categories_expense', PrivateCategoriesExpenseModelViewSets, basename='private_categories_expense')
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