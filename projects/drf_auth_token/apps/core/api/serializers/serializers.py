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
from apps.core.api.serializers.serializers_measure_units import (
    MeasureUnitsViewSerializer,
    MeasureUnitsActionsSerializer
)

class BulkDeleteSerializer(serializers.Serializer):
    ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="Lista de IDs a borrar."
    )