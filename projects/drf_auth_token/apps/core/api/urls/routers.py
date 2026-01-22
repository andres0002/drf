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
    PublicMeasureUnitsViewSets,
    PrivateMeasureUnitsModelViewSets
)

router = DefaultRouter()

# document types.
router.register(r'public_document_types', PublicDocumentTypesViewSets, basename='public_document_types')
router.register(r'private_document_types', PrivateDocumentTypesModelViewSets, basename='private_document_types')

# measure units.
router.register(r'public_measure_units', PublicMeasureUnitsViewSets, basename='public_measure_units')
router.register(r'private_measure_units', PrivateMeasureUnitsModelViewSets, basename='private_measure_units')

# instance urlpatterns.
urlpatterns = []
# populate instance.
urlpatterns += router.urls

# print('URLPATTERNS:', urlpatterns)
# for url in urlpatterns:
#     print(url)