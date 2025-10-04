# py
# django
# drf
from rest_framework.routers import DefaultRouter # type: ignore
# third
# own
from apps.features.user.api.viewsets.viewsets import (
    PublicGroupsViewSets,
    PrivateGroupsModelViewSets,
    PublicUserPermissionsViewSets,
    PrivateUserPermissionsModelViewSets,
    PublicRolesViewSets,
    PrivateRolesModelViewSets,
    PublicUsersViewSets,
    PrivateUsersModelViewSets,
    PublicFingerprintsViewSets,
    PrivateFingerprintsModelViewSets,
    PublicAccessLogsViewSets,
    PrivateAccessLogsModelViewSets
)

router = DefaultRouter()

# groups.
router.register(r'public_groups', PublicGroupsViewSets, basename='public_groups')
router.register(r'private_groups', PrivateGroupsModelViewSets, basename='private_groups')
# permissions.
router.register(r'public_user_permissions', PublicUserPermissionsViewSets, basename='public_user_permissions')
router.register(r'private_user_permissions', PrivateUserPermissionsModelViewSets, basename='private_user_permissions')
# roles.
router.register(r'public_roles', PublicRolesViewSets, basename='public_roles')
router.register(r'private_roles', PrivateRolesModelViewSets, basename='private_roles')
# users.
router.register(r'public_users', PublicUsersViewSets, basename='public_users')
router.register(r'private_users', PrivateUsersModelViewSets, basename='private_users')
# fingerprints.
router.register(r'public_fingerprints', PublicFingerprintsViewSets, basename='public_fingerprints')
router.register(r'private_fingerprints', PrivateFingerprintsModelViewSets, basename='private_fingerprints')
# access logs.
router.register(r'public_access_logs', PublicAccessLogsViewSets, basename='public_access_logs')
router.register(r'private_access_logs', PrivateAccessLogsModelViewSets, basename='private_access_logs')

# instance urlpatterns.
urlpatterns = []
# populate instance.
urlpatterns += router.urls

# print('URLPATTERNS:', urlpatterns)
# for url in urlpatterns:
#     print(url)