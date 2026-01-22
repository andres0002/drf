# py
# django
# drf
# from rest_framework import serializers
# third
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer # type: ignore
# own

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass