# py
# django
# drf
from rest_framework import serializers
# third
# own

# Create your views here.

class TestUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=255)
    
    # show in list.
    def to_representation(self, instance):
        # flujo normal, show all o todo lo que se especifique en el fields.
        # return super().to_representation(instance)
        # flujo especifico, show solo los campos especificos.
        return {
            'nombre_de_user':instance['username'], # para modificar como se quiere ver la key, with .values().
            # 'nombre_de_user':instance.username, # para modificar como se quiere ver la key, with .all().
            'correo_electronico':instance['email'] # para modificar como se quiere ver la key, with .values().
            # 'correo_electronico':instance.email # para modificar como se quiere ver la key, with .all().
        }
    
    def validate_username(self, username): # se hace antes del validate.
        # code -> validation extra.
        print(f'validate_username -> username -> {username}')
        return username
    
    def validate_email(self, email): # se hace antes del validate.
        # code -> validation extra.
        print(f'validate_email -> email -> {email}')
        return email
    
    def validate(self, data): # se hace al último.
        # code -> validation extra.
        print(f'validate -> data -> {data}')
        return data

    def save(self, **kwargs):
        # code -> validation extra.
        if self.instance:
            return self.update(self.instance, self.validated_data)
        return self.create(self.validated_data)
    
    def create(self, validated_data):
        # Crear la nueva instancia
        # validated_data = Modelo.objects.create(**validated_data)
        return validated_data

    def update(self, instance, validated_data):
        # Actualizar la instancia existente
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

# views.py
# data = {
#     'username':'username',
#     'email':'username@yopmail.com'
# }
# data_serializer = TestUserSerializer(data=data) # save() -> sin instance.
# # data_serializer = TestUserSerializer(data, data=data) # save() -> con instance.
# if data_serializer.is_valid():
#     print('data validated.')
#     data_serializer.save()