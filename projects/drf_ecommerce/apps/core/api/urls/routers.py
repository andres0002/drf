# py
# django
# from django.urls import path
# drf
from rest_framework.routers import DefaultRouter # type: ignore
# third
# own
from apps.core.api.viewsets.viewsets import (
    PublicDocumentTypesViewSets,
    PrivateDocumentTypesModelViewSets,
    PublicPaymentTypesViewSets,
    PrivatePaymentTypesModelViewSets,
    PublicDiscountTypesViewSets,
    PrivateDiscountTypesModelViewSets
)

router = DefaultRouter()

# document types.
router.register(r'public_document_types', PublicDocumentTypesViewSets, basename='public_document_types')
router.register(r'private_document_types', PrivateDocumentTypesModelViewSets, basename='private_document_types')

# payment types.
router.register(r'public_payment_types', PublicPaymentTypesViewSets, basename='public_payment_types')
router.register(r'private_payment_types', PrivatePaymentTypesModelViewSets, basename='private_payment_types')

# discount types.
router.register(r'public_discount_types', PublicDiscountTypesViewSets, basename='public_discount_types')
router.register(r'private_discount_types', PrivateDiscountTypesModelViewSets, basename='private_discount_types')

# instance urlpatterns.
urlpatterns = []
# populate instance.
urlpatterns += router.urls

# print('URLPATTERNS:', urlpatterns)
# for url in urlpatterns:
#     print(url)