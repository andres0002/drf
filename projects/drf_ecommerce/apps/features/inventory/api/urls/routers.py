# py
# django
# from django.urls import path
# drf
from rest_framework.routers import DefaultRouter # type: ignore
# third
# own
from apps.features.inventory.api.viewsets.viewsets import (
    PublicInventoryMovementsViewSets,
    PrivateInventoryMovementsModelViewSets,
    PublicStocksViewSets,
    PrivateStocksModelViewSets
)

router = DefaultRouter()

# inventory movements.
router.register(r'public_inventory_movements', PublicInventoryMovementsViewSets, basename='public_inventory_movements')
router.register(r'private_inventory_movements', PrivateInventoryMovementsModelViewSets, basename='private_inventory_movements')
# stocks.
router.register(r'public_stocks', PublicStocksViewSets, basename='public_stocks')
router.register(r'private_stocks', PrivateStocksModelViewSets, basename='private_stocks')

# instance urlpatterns.
urlpatterns = []
# populate instance.
urlpatterns += router.urls

# print('URLPATTERNS:', urlpatterns)
# for url in urlpatterns:
#     print(url)