# py
from decimal import Decimal, ROUND_HALF_UP
# django
from django.db import models # type: ignore
# third
# owm
from apps.core.models import BaseModels, DocumentTypes, PaymentTypes
from apps.shared.models import Countries, Cities

# Create your models here.

class Customers(BaseModels):
    internal = models.BooleanField(
        default=False,
        help_text="Indica si el cliente es un usuario interno del sistema",
        verbose_name='Internal'
    )
    
    # Datos para clientes internos
    user = models.OneToOneField(
        'user.Users',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="customers",
        verbose_name='User'
    )
    
    # Datos para clientes externos
    document_type = models.ForeignKey(DocumentTypes, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Document Type')
    document = models.CharField('Document Number', max_length=20, unique=True, null=True, blank=True)
    name = models.CharField('Name', max_length=150, blank=True, null=True)
    lastname = models.CharField('Last Name', max_length=150, blank=True, null=True)
    email = models.EmailField('Email', max_length=255, null=True, blank=True)
    phone = models.CharField('Phone Number', max_length=15, null=True, blank=True)
    address = models.CharField('Address', max_length=200, blank=True, null=True)
    country = models.ForeignKey(
        Countries,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="customers",
        verbose_name="Country"
    )
    city = models.ForeignKey(
        Cities,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="customers",
        verbose_name="City"
    )

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        ordering = ['id']

    def __str__(self):
        if self.internal and self.user:
            return f"Internal Customer: {self.user.username} ({self.user.email})"
        full_name = f"{self.name or ''} {self.lastname or ''}".strip()
        return full_name or f"External Customer {self.document or ''} ({self.email or ''})"

class Sales(BaseModels):
    customer = models.ForeignKey(
        Customers,
        on_delete=models.CASCADE,
        related_name="sales",
        verbose_name='Customer'
    )
    # quién registró la venta
    user = models.ForeignKey( 
        'user.Users',
        on_delete=models.CASCADE,
        related_name="sales",
        verbose_name='User'
    )
    payment_type = models.ForeignKey(PaymentTypes, on_delete=models.PROTECT, verbose_name='Payment Type')
    date = models.DateField('Date', auto_now_add=True)
    total_value = models.DecimalField('Total', max_digits=10, decimal_places=2, default=0, editable=False)
    
    @property
    def total(self):
        """Calcula el total en base a los detalles de la venta."""
        total = sum([detail.subtotal for detail in self.sale_details.all()], Decimal(0))
        return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    class Meta:
        verbose_name = 'Sale'
        verbose_name_plural = 'Sales'
        ordering = ['-id']

    def __str__(self):
        return f"Sale {self.id} - {self.customer}"

    def save(self, *args, **kwargs):
        # actualiza el total antes de guardar
        self.total_value = self.total
        super().save(*args, **kwargs)

class SaleDetails(BaseModels):
    sale = models.ForeignKey(
        Sales,
        on_delete=models.CASCADE,
        related_name="sale_details",
        verbose_name='Sale'
    )
    product = models.ForeignKey(
        'product.Products',
        on_delete=models.CASCADE,
        related_name='sale_details',
        verbose_name='Product'
    )
    quantity = models.PositiveIntegerField('Quantity', default=1)
    price = models.DecimalField('Price', max_digits=10, decimal_places=2)
    subtotal_value = models.DecimalField('Subtotal', max_digits=10, decimal_places=2, default=0, editable=False)
    
    @property
    def subtotal(self):
        """Calcula el subtotal dinámicamente."""
        return (Decimal(self.quantity) * Decimal(self.price)).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )

    class Meta:
        verbose_name = 'Sale Detail'
        verbose_name_plural = 'Sale Details'
        ordering = ['id']

    def __str__(self):
        return f"{self.product} x {self.quantity} in Sale {self.sale.id}"

    def save(self, *args, **kwargs):
        # actualiza el subtotal antes de guardar
        self.subtotal_value = self.subtotal
        super().save(*args, **kwargs)