# py
# django
# drf
from rest_framework import serializers
# third
# own

class BulkDeleteSerializer(serializers.Serializer):
    ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="Lista de IDs a borrar."
    )