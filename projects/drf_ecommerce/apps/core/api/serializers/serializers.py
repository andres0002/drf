# py
# django
# drf
from rest_framework import serializers # type: ignore
# third
# own
from apps.core.api.serializers.serializers_document_types import (
    DocumentTypesViewSerializer,
    DocumentTypesActionsSerializer
)
from apps.core.api.serializers.serializers_payment_types import (
    PaymentTypesViewSerializer,
    PaymentTypesActionsSerializer
)
from apps.core.api.serializers.serializers_discount_types import (
    DiscountTypesViewSerializer,
    DiscountTypesActionsSerializer
)
from apps.core.api.serializers.serializers_movement_types import (
    MovementTypesViewSerializer,
    MovementTypesActionsSerializer
)
from apps.core.api.serializers.serializers_measure_units import (
    MeasureUnitsViewSerializer,
    MeasureUnitsActionsSerializer
)

class BulkDeleteSerializer(serializers.Serializer):
    ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="Lista de IDs a borrar."
    )