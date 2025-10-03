# py
# django
# from django.urls import path
# drf
from rest_framework.routers import DefaultRouter # type: ignore
# third
# own
from apps.features.cart.api.viewsets.viewsets import (
    PublicCartsViewSets,
    PrivateCartsModelViewSets,
    PublicCartItemsViewSets,
    PrivateCartItemsModelViewSets
)

router = DefaultRouter()

# carts.
router.register(r'public_carts', PublicCartsViewSets, basename='public_carts')
router.register(r'private_carts', PrivateCartsModelViewSets, basename='private_carts')
# cart items.
router.register(r'public_cart_items', PublicCartItemsViewSets, basename='public_cart_items')
router.register(r'private_cart_items', PrivateCartItemsModelViewSets, basename='private_cart_items')

# instance urlpatterns.
urlpatterns = []
# populate instance.
urlpatterns += router.urls

# print('URLPATTERNS:', urlpatterns)
# for url in urlpatterns:
#     print(url)