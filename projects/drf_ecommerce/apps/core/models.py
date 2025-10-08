# py
# django
from django.db import models # type: ignore
from django.utils import timezone # type: ignore
# drf
# third
from simple_history.models import HistoricalRecords # type: ignore
# own

# Create your models here.

# Manager personalizado (para manejar registros activos/inactivos)
class ActiveManager(models.Manager):
    """Custom manager to handle active and deleted records."""

    def get_queryset(self):
        """Sobrescribe el queryset para devolver solo activos por defecto."""
        return super().get_queryset().filter(is_active=True)

    def is_activated(self):
        """Return only active records."""
        return self.get_queryset()

    def is_deleted(self):
        """Return only deleted/inactive records."""
        return self.filter(is_active=False)

# Base general
class BaseModels(models.Model):
    """Model definition for BaseModels."""

    # TODO: Define fields here
    is_active = models.BooleanField('Activated/Deactivated', default=True)
    created_at = models.DateTimeField('Created At', auto_now_add=True)
    updated_at = models.DateTimeField('Updated At', auto_now=True)
    deleted_at = models.DateTimeField('Deleted At', null=True, blank=True)
    
    # 🚫 Histórico seguro (sin password ni last_login)
    historical = HistoricalRecords(user_model='user.Users', inherit=True, excluded_fields=['password', 'last_login'])
    
    # --- Auditoría de usuario ---
    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value
    
    # Manager personalizado
    objects = ActiveManager() # solo registros activos (uso por defecto)
    all_objects = models.Manager() # todos los registros (incluidos eliminados)
    
    # --- Soft delete automático ---
    def save(self, *args, **kwargs):
        if not self.is_active and self.deleted_at is None:
            # Si el registro se desactiva por primera vez, guarda la fecha de eliminación
            self.deleted_at = timezone.now()
        elif self.is_active and self.deleted_at is not None:
            # Si se reactiva, limpiamos la fecha de eliminación
            self.deleted_at = None

        super().save(*args, **kwargs)
    
    def soft_delete(self):
        """Desactiva el registro (soft delete)."""
        self.is_active = False
        self.save(update_fields=['is_active', 'deleted_at', 'updated_at'])

    def restore(self):
        """Restaura un registro previamente desactivado."""
        self.is_active = True
        self.save(update_fields=['is_active', 'deleted_at', 'updated_at'])

    class Meta:
        """Meta definition for BaseModels."""
        abstract = True
        verbose_name = 'Base Model'
        verbose_name_plural = 'Base Models'

# Catálogo base (reutilizable)
class BaseCatalogs(BaseModels):
    """Model definition for BaseCatalogs."""

    # TODO: Define fields here
    code = models.CharField('Code', max_length=50, unique=True)
    name = models.CharField('Name', max_length=100)
    description = models.TextField('Description', null=True, blank=True)

    class Meta:
        """Meta definition for BaseCatalogs."""
        abstract = True
        verbose_name = 'Base Catalog'
        verbose_name_plural = 'Base Catalogs'

    def __str__(self):
        """Unicode representation of BaseCatalogs."""
        return f"{self.code} - {self.name}"

# Tipos de documento
class DocumentTypes(BaseCatalogs):
    """Model definition for DocumentTypes"""
    
    # TODO: Define fields here
    # code -> Ej: CC, NIT, PASSPORT
    # name -> Ej: "Cédula de Ciudadanía"
    # description -> Ej: text

    class Meta:
        """Meta definition for DocumentTypes."""
        verbose_name = "Document Type"
        verbose_name_plural = "Document Types"
        ordering = ["code"]

# Tipos de pago
class PaymentTypes(BaseCatalogs):
    """Model definition for PaymentTypes."""

    # TODO: Define fields here
    # code -> Ej: CASH, CARD, TRANSFER
    # name -> Ej: "Efectivo", "Tarjeta", "Transferencia"
    # description -> Ej: text

    class Meta:
        """Meta definition for PaymentTypes."""
        verbose_name = 'Payment Type'
        verbose_name_plural = 'Payment Types'
        ordering = ["code"]

# Tipos de descuento
class DiscountTypes(BaseCatalogs):
    """Model definition for DiscountTypes."""
    
    # TODO: Define fields here
    # code -> Ej: "PERCENTAGE", "AMOUNT"
    # name -> Ej: "Descuento porcentual", "Descuento fijo"
    # description -> Ej: text
    
    class Meta:
        """Meta definition for DiscountTypes."""
        verbose_name = 'Discount Type'
        verbose_name_plural = 'Discount Types'
        ordering = ["code"]

# Tipos de movimiento
class MovementTypes(BaseCatalogs):
    """Model definition for MovementTypes."""

    # TODO: Define fields here
    # code -> Ej: "IN", "OUT", "ADJ", "TRF", "RES"
    # name -> Ej: "Ingreso", "Salida", "Ajuste, Transferencia, Reserva"
    # description -> Ej: text

    class Meta:
        """Meta definition for MovementTypes."""
        verbose_name = 'Movement Type'
        verbose_name_plural = 'Movement Types'
        ordering = ["code"]

# Unidades de medida
class MeasureUnits(BaseCatalogs):
    """Model definition for MeasureUnits."""

    # TODO: Define fields here
    # code -> Ej: KG, LT, UN"
    # name -> Ej: Kilogramo, Litro, Unidad"
    # description -> Ej: text

    class Meta:
        """Meta definition for MeasureUnits."""
        verbose_name = 'Measure Unit'
        verbose_name_plural = 'Measure Units'
        ordering = ["code"]