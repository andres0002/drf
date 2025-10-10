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
    PrivateStocksModelViewSets,
    PublicWarehousesViewSets,
    PrivateWarehousesModelViewSets,
    PublicWarehouseTransfersViewSets,
    PrivateWarehouseTransfersModelViewSets
)

router = DefaultRouter()

# inventory movements.
router.register(r'public_inventory_movements', PublicInventoryMovementsViewSets, basename='public_inventory_movements')
router.register(r'private_inventory_movements', PrivateInventoryMovementsModelViewSets, basename='private_inventory_movements')
# stocks.
router.register(r'public_stocks', PublicStocksViewSets, basename='public_stocks')
router.register(r'private_stocks', PrivateStocksModelViewSets, basename='private_stocks')
# warehouses.
router.register(r'public_warehouses', PublicWarehousesViewSets, basename='public_warehouses')
router.register(r'private_warehouses', PrivateWarehousesModelViewSets, basename='private_warehouses')
# warehouse transfer.
router.register(r'public_warehouse_transfers', PublicWarehouseTransfersViewSets, basename='public_warehouse_transfers')
router.register(r'private_warehouse_transfers', PrivateWarehouseTransfersModelViewSets, basename='private_warehouse_transfers')

# instance urlpatterns.
urlpatterns = []
# populate instance.
urlpatterns += router.urls

# print('URLPATTERNS:', urlpatterns)
# for url in urlpatterns:
#     print(url)