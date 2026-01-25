# py
from datetime import datetime
# django
from django.contrib.auth import authenticate
from django.contrib.sessions.models import Session
from django.conf import settings
# drf
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
# third
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from rest_framework_simplejwt.tokens import RefreshToken as RT, TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# own
from apps.features.auth_own.api.serializers.serializers import CustomTokenObtainPairSerializer
from apps.features.user.api.serializers.serializers import UsersViewSerializer

# Create your views here.

class Login(TokenObtainPairView):
    authentication_classes = []  # <- Desactiva autenticación automática
    permission_classes = (AllowAny,)
    
    serializer_class = CustomTokenObtainPairSerializer
    
    @swagger_auto_schema(
        tags=["🔹 Auth"],
        operation_id="auth_login",
        operation_description="Login de usuario y generación de tokens de access and refresh.",
        responses={
            200: openapi.Response(description="Inicio de sesión exitoso"),
            400: "Credenciales inválidas"
        }
    )
    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(
            username=username,
            password=password
        )
        if user:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                user_serializer = UsersViewSerializer(user)
                return Response({
                    'token': login_serializer.validated_data.get('access'),
                    'refresh_token': login_serializer.validated_data.get('refresh'),
                    'user': user_serializer.data,
                    "message": "Inicio de sesión exitoso."
                }, status=status.HTTP_200_OK)
            return Response({
                'error':'Username o Password incorrectos'
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'error':'Username o Password incorrectos'
        }, status=status.HTTP_400_BAD_REQUEST)

def clean_expired_tokens():
    now = datetime.now()
    BlacklistedToken.objects.filter(token__expires_at__lt=now).delete()
    OutstandingToken.objects.filter(expires_at__lt=now).delete()

class Logout(APIView):
    permission_classes = (IsAuthenticated,)
    
    @swagger_auto_schema(
        tags=["🔹 Auth"],
        operation_id="auth_logout",
        operation_description="Logout de usuario, elimina tokens de access and refresh.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Token de refresco'),
            },
            required=['refresh']
        ),
        responses={
            200: openapi.Response(description="Logout exitoso"),
            401: "Credenciales inválidas o no autenticado"
        }
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        refresh_token = request.data.get("refresh", '')
        token_message = "Token de refresh no proporcionado."
        
        if not refresh_token:
            return Response({
                'error': token_message
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Eliminar sesiones activas del usuario
        sessions = Session.objects.filter(expire_date__gte=datetime.now())
        deleted_sessions = 0

        for session in sessions:
            data = session.get_decoded()
            if str(user.id) == str(data.get('_auth_user_id')):
                session.delete()
                deleted_sessions += 1

        if refresh_token:
            try:
                token = RT(refresh_token)
                token.blacklist()
                token_message = "Token de refresh invalidado correctamente."
            except TokenError as e:
                token_message = f"Error al invalidar token: {str(e)}"
        
        # Limpieza de tokens solo en desarrollo
        if settings.DEBUG:
            clean_expired_tokens()
        
        return Response({
            "token_message": token_message,
            "session_message": f"{deleted_sessions} sesión(es) eliminada(s)."
        }, status=status.HTTP_200_OK)

class RefreshToken(TokenRefreshView):
    @swagger_auto_schema(
        tags=["🔹 Auth"],
        operation_id="auth_refresh_token",
        operation_description="Refrescar token JWT.",
        responses={
            200: openapi.Response(description="Token actualizado correctamente"),
            401: "Token inválido o expirado",
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)