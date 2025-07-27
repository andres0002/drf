# py
# django
# drf
from rest_framework.routers import DefaultRouter
# third
# own
from apps.features.user.api.viewsets.viewsets import (
    PublicGroupsViewSets,
    PrivateGroupsModelViewSets,
    PublicUserPermissionsViewSets,
    PrivateUserPermissionsModelViewSets,
    PublicUsersViewSets,
    PrivateUsersModelViewSets
)

router = DefaultRouter()

# groups.
router.register(r'public_groups', PublicGroupsViewSets, basename='public_groups')
router.register(r'private_groups', PrivateGroupsModelViewSets, basename='private_groups')
# permissions.
router.register(r'public_user_permissions', PublicUserPermissionsViewSets, basename='public_user_permissions')
router.register(r'private_user_permissions', PrivateUserPermissionsModelViewSets, basename='private_user_permissions')
# users.
router.register(r'public_users', PublicUsersViewSets, basename='public_users')
router.register(r'private_users', PrivateUsersModelViewSets, basename='private_users')

# instance urlpatterns.
urlpatterns = []
# populate instance.
urlpatterns += router.urls

# print('URLPATTERNS:', urlpatterns)
# for url in urlpatterns:
#     print(url)