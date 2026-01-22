# py
# django
# from django.urls import path
# drf
from rest_framework.routers import DefaultRouter # type: ignore
# third
# own
from apps.shared.api.viewsets.viewsets import (
    PublicCountriesViewSets,
    PrivateCountriesModelViewSets,
    PublicCitiesViewSets,
    PrivateCitiesModelViewSets
)

router = DefaultRouter()

# countries.
router.register(r'public_countries', PublicCountriesViewSets, basename='public_countries')
router.register(r'private_countries', PrivateCountriesModelViewSets, basename='private_countries')

# cities.
router.register(r'public_cities', PublicCitiesViewSets, basename='public_cities')
router.register(r'private_cities', PrivateCitiesModelViewSets, basename='private_cities')

# instance urlpatterns.
urlpatterns = []
# populate instance.
urlpatterns += router.urls

# print('URLPATTERNS:', urlpatterns)
# for url in urlpatterns:
#     print(url)