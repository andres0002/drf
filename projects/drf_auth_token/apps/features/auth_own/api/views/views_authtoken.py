# py
from datetime import datetime
# django
from django.contrib.sessions.models import Session
# drf
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import get_authorization_header
# third
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
# own
from apps.features.auth_own.authentication import ExpiringTokenAuthentication
from apps.features.user.api.serializers.serializers import UsersViewSerializer

# Create your views here.

# Authorization Token {token_key}

class Login(ObtainAuthToken):
    authentication_classes = []  # <- Desactiva autenticación automática
    permission_classes = (AllowAny,)
    
    @swagger_auto_schema(
        tags=["🔹 Auth"],
        operation_id="auth_login",
        operation_description="Login de usuario y generación de token.",
        responses={
            200: openapi.Response(description="Inicio de sesión exitoso"),
            400: "Credenciales inválidas",
            401: "Usuario inactivo",
            409: "Usuario ya autenticado"
        }
    )
    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(data=request.data, context={'request':request})
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                user_serializer = UsersViewSerializer(user)
                if created:
                    return Response({
                        "token": token.key,
                        "user": user_serializer.data,
                        "message": "Inicio de sesión exitoso."
                    }, status=status.HTTP_200_OK)
                else:
                    # Eliminar sesiones activas del usuario
                    sessions = Session.objects.filter(expire_date__gte=datetime.now())
                    deleted_sessions = 0

                    for session in sessions:
                        data = session.get_decoded()
                        if str(user.id) == str(data.get('_auth_user_id')):
                            session.delete()
                            deleted_sessions += 1
                    
                    # Eliminar el token del usuario
                    token.delete()
                    
                    # create token.
                    token = Token.objects.create(user=user)
                    
                    return Response({
                        "token": token.key,
                        "user": user_serializer.data,
                        "message": "Inicio de sesión exitoso."
                    }, status=status.HTTP_200_OK)
            else:
                return Response({'error':'Este usuario no puede iniciar sesión.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'error':'Username o Password incorrectos'}, status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    permission_classes = (IsAuthenticated,)
    
    @swagger_auto_schema(
        tags=["🔹 Auth"],
        operation_id="auth_logout",
        operation_description="Logout de usuario, elimina token y sesiones activas.",
        responses={
            200: openapi.Response(description="Logout exitoso"),
            401: "Credenciales inválidas o no autenticado"
        }
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        
        token = Token.objects.filter(user=user).first()
        
        # Eliminar sesiones activas del usuario
        sessions = Session.objects.filter(expire_date__gte=datetime.now())
        deleted_sessions = 0

        for session in sessions:
            data = session.get_decoded()
            if str(user.id) == str(data.get('_auth_user_id')):
                session.delete()
                deleted_sessions += 1
        
        # Eliminar el token del usuario
        token.delete()
        
        return Response({
            "token_message": "Token eliminado correctamente.",
            "session_message": f"{deleted_sessions} sesión(es) eliminada(s)."
        }, status=status.HTTP_200_OK)

class RefreshToken(APIView):
    authentication_classes = []  # <- Desactiva autenticación automática
    # Permitimos el acceso sin autenticación para poder recibir tokens expirados
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        tags=["🔹 Auth"],
        operation_id="auth_refresh_token",
        operation_description="Actualización de token. Requiere token en encabezado Authorization, aunque esté expirado.",
        manual_parameters=[
            openapi.Parameter(
                name='Authorization',
                in_=openapi.IN_HEADER,
                description='Token de autenticación. Formato: Token {tu_token}',
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Token actualizado correctamente",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "token": openapi.Schema(type=openapi.TYPE_STRING, description="Token renovado"),
                        "user": openapi.Schema(type=openapi.TYPE_OBJECT, description="Datos del usuario"),
                        "message": openapi.Schema(type=openapi.TYPE_STRING, description="Mensaje de estado"),
                    }
                )
            ),
            401: openapi.Response(description="Token inválido o no proporcionado"),
        }
    )
    def get(self, request, *args, **kwargs):
        auth_header = get_authorization_header(request).split()
        if not auth_header or len(auth_header) != 2:
            return Response({
                "detail": "No se proporcionó token"
            }, status=status.HTTP_401_UNAUTHORIZED)

        token_key = auth_header[1].decode()
        try:
            token = Token.objects.select_related('user').get(key=token_key)
            user = token.user
        except Token.DoesNotExist:
            return Response({
                "detail": "Token inválido"
            }, status=status.HTTP_401_UNAUTHORIZED)

        expiring_auth = ExpiringTokenAuthentication()
        token, token_expired = expiring_auth.token_expire_handler(token, Token, user)
        if token_expired:
            # se elimina el token.
            token.delete()
            # se actualiza el token sin necesidad de cerrar las sessions.
            token = Token.objects.create(user=user)

        user_serializer = UsersViewSerializer(user)
        return Response({
            "token": token.key,
            "user": user_serializer.data,
            "message": "Token actualizado correctamente"
        }, status=status.HTTP_200_OK)