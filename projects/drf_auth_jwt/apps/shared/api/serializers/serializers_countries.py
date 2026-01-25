# py
# django
# drf
from rest_framework import serializers # type: ignore
# third
# own
from apps.shared.models import Countries

class CountriesViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = '__all__'

class CountriesActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        exclude = ('id','is_active','created_at','updated_at','deleted_at')