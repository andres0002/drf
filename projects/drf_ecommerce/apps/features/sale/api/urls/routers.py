# py
# django
# from django.urls import path
# drf
from rest_framework.routers import DefaultRouter # type: ignore
# third
# own
from apps.features.sale.api.viewsets.viewsets import (
    PublicCustomersViewSets,
    PrivateCustomersModelViewSets,
    PublicSalesViewSets,
    PrivateSalesModelViewSets,
    PublicSaleDetailsViewSets,
    PrivateSaleDetailsModelViewSets
)

router = DefaultRouter()

# customers.
router.register(r'public_customers', PublicCustomersViewSets, basename='public_customers')
router.register(r'private_customers', PrivateCustomersModelViewSets, basename='private_customers')
# sales.
router.register(r'public_sales', PublicSalesViewSets, basename='public_sales')
router.register(r'private_sales', PrivateSalesModelViewSets, basename='private_sales')
# sale details.
router.register(r'public_sale_details', PublicSaleDetailsViewSets, basename='public_sale_details')
router.register(r'private_sale_details', PrivateSaleDetailsModelViewSets, basename='private_sale_details')

# instance urlpatterns.
urlpatterns = []
# populate instance.
urlpatterns += router.urls

# print('URLPATTERNS:', urlpatterns)
# for url in urlpatterns:
#     print(url)