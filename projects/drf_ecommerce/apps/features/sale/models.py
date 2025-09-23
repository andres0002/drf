# py
# django
from django.db import models # type: ignore
# third
# owm
from apps.core.models import BaseModels, DocumentTypes, PaymentTypes

# Create your models here.

class Customers(BaseModels):
    internal = models.BooleanField(
        default=False,
        help_text="Indica si el cliente es un usuario interno del sistema"
    )
    
    # Datos para clientes internos
    user = models.OneToOneField(
        'user.Users',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="customer_profile"
    )
    
    # Datos para clientes externos
    document_type = models.ForeignKey(DocumentTypes, on_delete=models.PROTECT, null=True, blank=True)
    document = models.CharField('Document Number', max_length=20, unique=True, null=True, blank=True)
    name = models.CharField('Name', max_length=150, blank=True, null=True)
    lastname = models.CharField('Last Name', max_length=150, blank=True, null=True)
    email = models.EmailField('Email', max_length=255, null=True, blank=True)
    phone = models.CharField('Phone Number', max_length=15, null=True, blank=True)
    address = models.CharField('Address', max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        ordering = ['id']

    def __str__(self):
        if self.internal and self.user:
            return f"Internal Customer: {self.user.username} ({self.user.email})"
        return self.name or f"External Customer {self.document} ({self.email})"

class Sales(BaseModels):
    customer = models.ForeignKey(
        Customers,
        on_delete=models.CASCADE,
        related_name="sales"
    )
    user = models.ForeignKey(  # quién registró la venta
        'user.Users',
        on_delete=models.CASCADE,
        related_name="sales_created"
    )
    payment_type = models.ForeignKey(PaymentTypes, on_delete=models.PROTECT)
    date = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Sale'
        verbose_name_plural = 'Sales'
        ordering = ['id']

    def __str__(self):
        return f"Sale {self.id} - {self.customer}"

class SaleDetails(BaseModels):
    sale = models.ForeignKey(
        Sales,
        on_delete=models.CASCADE,
        related_name="details"
    )
    product = models.ForeignKey(
        'inventory.Product',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Sale Detail'
        verbose_name_plural = 'Sale Details'
        ordering = ['id']

    def __str__(self):
        return f"{self.product} x{self.quantity} in {self.sale}"