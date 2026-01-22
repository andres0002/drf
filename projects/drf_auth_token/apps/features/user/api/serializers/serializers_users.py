# py
# django
from django.contrib.auth.models import Group, Permission
# drf
from rest_framework import serializers
# third
# own
from apps.features.user.models import Users
from apps.features.user.api.serializers.serializers import (
    GroupsViewSerializer,
    UserPermissionsViewSerializer
)

class UsersViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = ('deleted_at','is_active','is_staff','is_superuser','password')
    
    groups = GroupsViewSerializer(many=True, read_only=True)
    user_permissions = UserPermissionsViewSerializer(many=True, read_only=True)

class UsersActionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = ('id','is_active','is_staff','is_superuser','last_login','created_at','updated_at','deleted_at')
    
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True, required=False)
    
    # READ: Mostrar grupos y permisos anidados
    groups = GroupsViewSerializer(many=True, read_only=True)
    user_permissions = UserPermissionsViewSerializer(many=True, read_only=True)
    
    # WRITE: Enviar solo los IDs
    group_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Group.objects.all(),
        write_only=True,
        source='groups',
        required=False
    )
    permission_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Permission.objects.all(),
        write_only=True,
        source='user_permissions',
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Detecta si es creación (POST), no hay instance.
        if self.instance is None:
            self.fields['username'].required = True
            self.fields['email'].required = True
            self.fields['password'].required = True
    
    def create(self, validated_data):
        # obtine el password y lo elimina del context, para que no se guarde como text palno.
        password = validated_data.pop('password', None)
        groups = validated_data.pop('groups', [])
        permissions = validated_data.pop('user_permissions', [])
        user = Users(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        if groups:
            user.groups.set(groups)
        if permissions:
            user.user_permissions.set(permissions)
        return user

    def update(self, instance, validated_data):
        # obtine el password y lo elimina del context, para que no se guarde como text palno.
        password = validated_data.pop('password', None)
        groups = validated_data.pop('groups', None)
        permissions = validated_data.pop('user_permissions', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        if groups is not None:
            instance.groups.set(groups)
        if permissions is not None:
            instance.user_permissions.set(permissions)
        return instance

class UsersChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=5, max_length=128, write_only=True)
    password2 = serializers.CharField(min_length=5, max_length=128, write_only=True)
    
    def validate(self, data):
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError({'field': 'Las contraseñas no son iguales.'})
        return data

class UsersResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class UsersResetPasswordConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, data):
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError({'field': 'Las contraseñas no son iguales.'})
        return data