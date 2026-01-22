# py
from datetime import timedelta
from datetime import datetime
# django
from django.utils import timezone
from django.conf import settings
from django.contrib.sessions.models import Session
# drf
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, get_authorization_header, BaseAuthentication
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import AuthenticationFailed
# third
# own

class ExpiringTokenAuthentication(TokenAuthentication):
    
    # calculo tiempo de expiración.
    def expires_in(self, token):
        time_elapsed = timezone.now() - token.created
        left_time = timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
        return left_time
    
    # validate si el token ya expired.
    def is_token_expired(self, token):
        return self.expires_in(token) < timedelta(seconds=0)
    
    # si token ya esta expirado.
    def token_expire_handler(self, token, model, user):
        # expired = False
        is_expired = self.is_token_expired(token)
        # if is_expired:
            # logical de si el token ya expiro.
            # token.delete()
            # se actualiza el token sin necesidad de cerrar las sessions.
            # token = model.objects.create(user=user)
            # indica que el token a expirado.
            # expired = True
        return (token, is_expired)
    
    def authenticate_credentials(self, key):
        user, token = None, None
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
            user = token.user
            token, token_expired = self.token_expire_handler(token, model, user)
            if token_expired:
                raise AuthenticationFailed('Token inválido o expirado.')
            user = token.user
        except model.DoesNotExist:
            raise AuthenticationFailed('Token inválido o expirado.')
        
        return (user, token)

class CustomAuthentication(BaseAuthentication):
    user, token = None, None
    
    def get_user(self, request):
        token = get_authorization_header(request).split()
        if token:
            try:
                token = token[1].decode()
            except:
                return (None, None)
            
            token_expire = ExpiringTokenAuthentication()
            user, token = token_expire.authenticate_credentials(token)
            
            if user != None and token != None:
                self.user = user
                self.token = token
                return (user, token)
            
        return (None, None)
    
    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or len(auth) != 2:
            # Correcto: indica que no se autenticó y se sigue evaluando otras clases de auth
            return None  # No se envió token → permite continuar (por ejemplo, en login) o endpoints publics.
        self.get_user(request)
        if self.user is None and self.token is None:
            raise AuthenticationFailed('No se han enviado las credentials.')
        return (self.user, self.token)