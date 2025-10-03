# py
# django
# from django.urls import path
# drf
from rest_framework.routers import DefaultRouter # type: ignore
# third
# own
from apps.features.product.api.viewsets.viewsets import (
    PublicProductCategoriesViewSets,
    PrivateProductCategoriesModelViewSets,
    PublicPromotionsViewSets,
    PrivatePromotionsModelViewSets,
    PublicProductsViewSets,
    PrivateProductsModelViewSets,
    PublicProductComponentsViewSets,
    PrivateProductComponentsModelViewSets
)

router = DefaultRouter()

# product categories.
router.register(r'public_product_categories', PublicProductCategoriesViewSets, basename='public_product_categories')
router.register(r'private_product_categories', PrivateProductCategoriesModelViewSets, basename='private_product_categories')
# promotions.
router.register(r'public_promotions', PublicPromotionsViewSets, basename='public_promotions')
router.register(r'private_promotions', PrivatePromotionsModelViewSets, basename='private_promotions')
# products.
router.register(r'public_products', PublicProductsViewSets, basename='public_products')
router.register(r'private_products', PrivateProductsModelViewSets, basename='private_products')
# product components.
router.register(r'public_product_components', PublicProductComponentsViewSets, basename='public_product_components')
router.register(r'private_product_components', PrivateProductComponentsModelViewSets, basename='private_product_components')

# instance urlpatterns.
urlpatterns = []
# populate instance.
urlpatterns += router.urls

# print('URLPATTERNS:', urlpatterns)
# for url in urlpatterns:
#     print(url)