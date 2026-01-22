# py
# django
# drf
# third
# own
from apps.features.user.api.serializers.serializers_groups import (
    GroupsViewSerializer,
    GroupsActionsSerializer
)
from apps.features.user.api.serializers.serializers_permissions import (
    UserPermissionsViewSerializer,
    UserPermissionsActionsSerializer
)
from apps.features.user.api.serializers.serializers_roles import (
    RolesViewSerializer,
    RolesActionsSerializer
)
from apps.features.user.api.serializers.serializers_users import (
    UsersViewSerializer,
    UsersActionsSerializer,
    UsersChangePasswordSerializer,
    UsersResetPasswordRequestSerializer,
    UsersResetPasswordConfirmSerializer
)
from apps.features.user.api.serializers.serializers_fingerprints import (
    FingerprintsViewSerializer,
    FingerprintsActionsSerializer
)
from apps.features.user.api.serializers.serializers_access_logs import (
    AccessLogsViewSerializer,
    AccessLogsActionsSerializer
)