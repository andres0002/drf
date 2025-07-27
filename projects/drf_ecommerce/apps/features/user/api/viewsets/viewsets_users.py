# py
import logging
# django
from django.utils.http import (
    urlsafe_base64_encode,
    urlsafe_base64_decode
)
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
# drf
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
# third
from drf_yasg import openapi # type: ignore
from drf_yasg.utils import swagger_auto_schema # type: ignore
# own
from apps.core.api.viewsets.viewsets import (
    PublicGeneralViewSets,
    PrivateGeneralModelViewSets
)
from apps.features.user.api.serializers.serializers import (
    UsersViewSerializer,
    UsersActionsSerializer,
    UsersChangePasswordSerializer,
    UsersResetPasswordRequestSerializer,
    UsersResetPasswordConfirmSerializer
)
from apps.core.utils.emails import send_email_general

# Create your views here.

# __name__ -> 'apps.features.user.api.viewsets.viewsets_users'
logger = logging.getLogger(__name__)

class PublicUsersViewSets(PublicGeneralViewSets):
    serializer_class = UsersActionsSerializer
    serializer_view_class = UsersViewSerializer
    
    def list(self, request, *args, **kwargs):
        users = self.get_queryset()
        users_serializer = self.get_serializer(users, many = True)
        return Response(users_serializer.data,status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        method='post',
        request_body=UsersResetPasswordRequestSerializer,
        responses={
            200: openapi.Response(description="Si el email está registrado, se ha enviado un enlace de restablecimiento."),
            400: openapi.Response(description="Solicitud inválida."),
        },
        # operation_summary="Solicitar restablecimiento de contraseña",
        operation_description="Envía un enlace de restablecimiento si el email está registrado en el sistema."
    )
    @action(detail=False, methods=['post'])
    def reset_password_request(self, request):
        email_serializer = UsersResetPasswordRequestSerializer(data=request.data)
        
        # url -> debe ser la del frontend, en este coso puse la del backend por el momento.
        url_base = request.build_absolute_uri()
        
        if email_serializer.is_valid():
            email = email_serializer.validated_data.get('email')
            model = self.get_serializer_class().Meta.model
            user = model.objects.filter(email=email).first()
            
            try:
                if not user:
                    raise model.DoesNotExist(f"User with email {email} does not exist")
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                # url -> debe ser la del frontend, en este coso puse la del backend por el momento.
                # url_base ->  http://127.0.0.1:8000/user/public_users/reset_password_confirm/
                reset_link = f"{url_base}?uid={uid}&token={token}/"
                # logica de envio de email.
                ok, error = send_email_general(
                    subject=f'Reset Password Request -> {user.name} {user.lastname}',
                    body={
                        'template_name':'reset_password_request_email.html',
                        'context':{
                            'name': f'{user.name} {user.lastname}',
                            'email': user.email,
                            'content': f"Link de recuperación de password: {reset_link}"
                        }
                    },
                    to=[user.email],
                    reply_to=[user.email]
                )
                if ok:
                    logger.info(f'Mail send successfully -> Data -> Name: {user.name} {user.lastname}, email: {user.email}, content: Link de recuperación de password: {reset_link}.')
                else:
                    logger.error(f'Mail send errorfully -> Data -> Name: {user.name} {user.lastname}, email: {user.email}, content: Link de recuperación de password: {reset_link}, error: {error}.')
                # import pdb; pdb.set_trace() # para debugear.
            except model.DoesNotExist:
                pass # No revelar si el correo existe.
            
            return Response({
                'detail': 'Si el email está registrado, se ha enviado un enlace de restablecimiento.'
            }, status=status.HTTP_200_OK)
        
        return Response(email_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        method='post',
        request_body=UsersResetPasswordConfirmSerializer,
        responses={
            200: openapi.Response(description="Contraseña restablecida correctamente"),
            400: openapi.Response(description="Token inválido, UID incorrecto, contraseñas distintas o error de validación"),
        },
        # operation_summary="Confirmar restablecimiento de contraseña",
        operation_description="Confirma el restablecimiento de contraseña usando el UID y token enviados al correo. Requiere dos campos de contraseña iguales.",
    )
    @action(detail=False, methods=['post'])
    def reset_password_confirm(self, request):
        serializer = UsersResetPasswordConfirmSerializer(data=request.data)
        if serializer.is_valid():
            uid = serializer.validated_data.get('uid')
            token = serializer.validated_data.get('token')
            password = serializer.validated_data.get('password')

            model = self.get_serializer_class().Meta.model

            try:
                uid = urlsafe_base64_decode(uid).decode()
                user = model.objects.filter(pk=uid).first()
            except (model.DoesNotExist, ValueError, TypeError, OverflowError):
                return Response({'detail': 'UID inválido.'}, status=status.HTTP_400_BAD_REQUEST)

            if not default_token_generator.check_token(user, token):
                return Response({'detail': 'Token inválido o expirado.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # import pdb; pdb.set_trace() # para debugear.

            # Cambiar la contraseña
            user.set_password(password)
            user.save()

            return Response({'detail': 'Contraseña restablecida correctamente'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PrivateUsersModelViewSets(PrivateGeneralModelViewSets):
    serializer_view_class = UsersViewSerializer
    serializer_class = UsersActionsSerializer
    
    # elimination logical -> si se quiere eliminar de forma directa solo comentar el method destroy().
    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user:
            user.is_active = False
            user.save()
            return Response({'message':'Successfully User elimination.'},status=status.HTTP_200_OK)
        return Response({'messge':'Errorful User elimination.'},status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        request_body=UsersChangePasswordSerializer,
        responses={
            200: openapi.Response(description='Password actualizada correctamente.'),
            400: openapi.Response(description='Error de validación en la información enviada.')
        },
        # operation_summary="Actualizar contraseña del usuario", # comment endpoint.
        operation_description="Permite actualizar la contraseña del usuario autenticado usando su ID."
    )
    # detail in False -> para poner el enpoint direct "/user/private_users/set_password/"
    # detail in True -> para poner el enpoint despues del detail "/user/private_users/{id}/set_password/"
    @action(detail=True, methods=['post'])
    def change_password(self, request, *args, **kwargs):
        user = self.get_object()
        passwords_serializer = UsersChangePasswordSerializer(data=request.data)
        if passwords_serializer.is_valid():
            user.set_password(passwords_serializer.validated_data.get('password'))
            user.save()
            return Response({
                'message': 'Password de user actualizada successfully.'
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Hay errores en la info enviada.',
            'errors': passwords_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)