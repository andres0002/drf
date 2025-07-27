# py
from datetime import datetime
# django
from django.core.management.base import BaseCommand
# drf
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

class Command(BaseCommand):
    help = 'Elimina tokens JWT expirados (Outstanding y Blacklisted) para liberar recursos'

    def handle(self, *args, **kwargs):
        now = datetime.now()

        # Eliminar tokens blacklisteados y expirados
        blacklisted_deleted, _ = BlacklistedToken.objects.filter(token__expires_at__lt=now).delete()

        # Eliminar tokens outstanding expirados
        outstanding_deleted, _ = OutstandingToken.objects.filter(expires_at__lt=now).delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Tokens eliminados:\n"
                f"- Blacklisted: {blacklisted_deleted}\n"
                f"- Outstanding: {outstanding_deleted}"
            )
        )

# comman execute in console.
# python manage.py cleantokens
# py manage.py cleantokens