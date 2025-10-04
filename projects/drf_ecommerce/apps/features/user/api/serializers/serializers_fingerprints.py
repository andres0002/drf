# py
# django
# drf
from rest_framework import serializers # type: ignore
# third
# own
from apps.features.user.models import Fingerprints

class FingerprintsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fingerprints
        fields = '__all__'

class FingerprintsActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fingerprints
        exclude = ('id','is_active','created_at','updated_at','deleted_at')