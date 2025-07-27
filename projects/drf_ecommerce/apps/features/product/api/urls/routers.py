# py
# django
# from django.urls import path
# drf
from rest_framework.routers import DefaultRouter
# third
# own
from apps.features.product.api.viewsets.viewsets import (
    PublicMeasureUnitsViewSets,
    PrivateMeasureUnitsModelViewSets,
    PublicCategoriesProductViewSets,
    PrivateCategoriesProductModelViewSets,
    PublicIndicatorsViewSets,
    PrivateIndicatorsModelViewSets,
    PublicProductsViewSets,
    PrivateProductsModelViewSets
)

router = DefaultRouter()

# measure units.
router.register(r'public_measure_units', PublicMeasureUnitsViewSets, basename='public_measure_units')
router.register(r'private_measure_units', PrivateMeasureUnitsModelViewSets, basename='private_measure_units')
# categories product.
router.register(r'public_categories_product', PublicCategoriesProductViewSets, basename='public_categories_product')
router.register(r'private_categories_product', PrivateCategoriesProductModelViewSets, basename='private_categories_product')
# indicators.
router.register(r'public_indicators', PublicIndicatorsViewSets, basename='public_indicators')
router.register(r'private_indicators', PrivateIndicatorsModelViewSets, basename='private_indicators')
# products.
router.register(r'public_products', PublicProductsViewSets, basename='public_products')
router.register(r'private_products', PrivateProductsModelViewSets, basename='private_products')

# instance urlpatterns.
urlpatterns = []
# populate instance.
urlpatterns += router.urls

# print('URLPATTERNS:', urlpatterns)
# for url in urlpatterns:
#     print(url)