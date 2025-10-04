# py
# django
from django.db import models # type: ignore
# drf
# third
from simple_history.models import HistoricalRecords # type: ignore
# own

# Create your models here.

class BaseModels(models.Model):
    """Model definition for BaseModels."""

    # TODO: Define fields here
    is_active = models.BooleanField('Activated/Deactivated', default=True)
    created_at = models.DateTimeField('Created At', auto_now_add=True)
    updated_at = models.DateTimeField('Updated At', auto_now=True)
    deleted_at = models.DateTimeField('Deleted At', auto_now=True, null=True, blank=True)
    
    # 🚫 Histórico seguro (sin password ni last_login)
    historical = HistoricalRecords(user_model='user.Users', inherit=True, excluded_fields=['password', 'last_login'])
    
    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        """Meta definition for BaseModels."""

        abstract = True
        verbose_name = 'BaseModel'
        verbose_name_plural = 'BaseModels'

class DocumentTypes(BaseModels):
    """Model definition for DocumentTypes (DNI, RUC, Passport, etc.)"""
    code = models.CharField(max_length=20, unique=True)   # Ej: CC, NIT, PASSPORT
    name = models.CharField(max_length=100)              # Ej: "Cédula de Ciudadanía"
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Document Type"
        verbose_name_plural = "Document Types"
        ordering = ["id"]

    def __str__(self):
        return f"{self.code} - {self.description}"

class PaymentTypes(BaseModels):
    """Model definition for PaymentTypes."""

    # TODO: Define fields here
    code = models.CharField(max_length=50, unique=True)   # Ej: CASH, CARD, TRANSFER
    name = models.CharField(max_length=100)              # Ej: "Efectivo", "Tarjeta", "Transferencia"
    description = models.TextField(null=True, blank=True)

    class Meta:
        """Meta definition for PaymentTypes."""

        verbose_name = 'Payment Type'
        verbose_name_plural = 'Payment Types'
        ordering = ['id']

    def __str__(self):
        """Unicode representation of PaymentTypes."""
        return self.name

class DiscountTypes(BaseModels):
    """Model definition for DiscountTypes."""
    
    # TODO: Define fields here
    code = models.CharField(max_length=50, unique=True)   # Ej: "PERCENTAGE", "AMOUNT"
    name = models.CharField(max_length=100)               # Ej: "Descuento porcentual", "Descuento fijo"
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        """Meta definition for DiscountTypes."""

        verbose_name = 'Discount Type'
        verbose_name_plural = 'Discount Types'
        ordering = ['id']

    def __str__(self):
        """Unicode representation of DiscountTypes."""
        return f"{self.name} ({self.code})"

class MovementTypes(BaseModels):
    """Model definition for MovementTypes."""

    code = models.CharField(max_length=50, unique=True)   # Ej: "IN", "OUT", "ADJ", "TRF", "RES"
    name = models.CharField(max_length=100)               # Ej: "Ingreso", "Salida", "Ajuste, Transferencia, Reserva"
    description = models.TextField(blank=True, null=True)

    class Meta:
        """Meta definition for MovementTypes."""
        verbose_name = 'Movement Type'
        verbose_name_plural = 'Movement Types'
        ordering = ['id']

    def __str__(self):
        """Unicode representation of MovementTypes."""
        return f"{self.name} ({self.code})"

class MeasureUnits(BaseModels):
    """Model definition for MeasureUnits."""

    # TODO: Define fields here
    code = models.CharField(
        max_length=50,
        unique=True,
        help_text="Código único de la unidad de medida. Ej: KG, LT, UN"
    )
    name = models.CharField(
        max_length=100,
        help_text="Nombre de la unidad de medida. Ej: Kilogramo, Litro, Unidad"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Descripción detallada de la unidad de medida"
    )

    class Meta:
        """Meta definition for MeasureUnits."""

        verbose_name = 'Measure Unit'
        verbose_name_plural = 'Measure Units'
        ordering = ['id']

    def __str__(self):
        """Unicode representation of MeasureUnits."""
        return f"{self.name} ({self.code})"
