# py
from decimal import Decimal
# django
from django.db import models # type: ignore
# drf
# third
# own
from apps.core.models import BaseModels, PaymentTypes
from apps.features.product.models import Products

# Create your models here.

class Suppliers(BaseModels):
    """Model definition for Suppliers."""

    # TODO: Define fields here
    ruc = models.CharField('Ruc', unique=True, max_length=11)
    business_name = models.CharField('Comapny Name', max_length=150)
    address = models.CharField('Address', max_length=200)
    phone = models.CharField('Phone Number', max_length=15, null=True, blank=True)
    email = models.EmailField('Email', max_length=255, null=True, blank=True)

    class Meta:
        """Meta definition for Suppliers."""
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
        ordering = ['id']

    def __str__(self):
        """Unicode representation of Suppliers."""
        return f"{self.ruc} - {self.business_name}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'ruc': self.ruc,
            'business_name': self.business_name,
            'address': self.address,
            'phone': self.phone,
            'email': self.email
        }

class Vouchers(BaseModels):
    """Model definition for Vouchers."""

    # TODO: Define fields here
    name = models.CharField('Payment Voucher Name', max_length=100, unique=True)

    class Meta:
        """Meta definition for Vouchers."""
        verbose_name = 'Voucher'
        verbose_name_plural = 'Vouchers'
        ordering = ['id']

    def __str__(self):
        """Unicode representation of Vouchers."""
        return self.name

class ExpenseCategories(BaseModels):
    """Model definition for ExpenseCategories."""

    # TODO: Define fields here
    code = models.CharField('Code', max_length=50, unique=True)
    name = models.CharField('Name', max_length=100)
    description = models.CharField('Description', max_length=150, blank=True, null=True)

    class Meta:
        """Meta definition for ExpenseCategories."""
        verbose_name = 'Expense Category'
        verbose_name_plural = 'Expense Categories'
        ordering = ['id']

    def __str__(self):
        """Unicode representation of ExpenseCategories."""
        return f"{self.code} - {self.name}"

class Expenses(BaseModels):
    """Model definition for Expenses."""

    # TODO: Define fields here
    date = models.DateField('Fecha de Emisión de Factura')
    quantity = models.DecimalField('Quantity', max_digits=10, decimal_places=2)
    unit_price = models.DecimalField('Precio Unitario', max_digits=10, decimal_places=2, default=0)
    voucher_number = models.CharField('Número de Comprobante', max_length=50, unique=True)
    total = models.DecimalField('Total', max_digits=14, decimal_places=2, default=0)
    voucher = models.ForeignKey(Vouchers, on_delete=models.PROTECT)
    user = models.ForeignKey('user.Users', on_delete=models.PROTECT)
    supplier = models.ForeignKey(Suppliers, on_delete=models.PROTECT)
    payment_type = models.ForeignKey(PaymentTypes, on_delete=models.PROTECT)
    product = models.ForeignKey(Products, on_delete=models.PROTECT, related_name="expenses")
    category = models.ForeignKey(ExpenseCategories, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        """Meta definition for Expenses."""
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'
        ordering = ['-date']

    def clean(self):
        from django.core.exceptions import ValidationError # type: ignore
        if self.quantity <= 0:
            raise ValidationError("La cantidad debe ser mayor que cero.")
        if self.unit_price < 0:
            raise ValidationError("El precio unitario no puede ser negativo.")

    def save(self, *args, **kwargs):
        self.full_clean()
        # luego tu lógica
        # Recalcula el total antes de guardar
        self.total = Decimal(self.quantity) * Decimal(self.unit_price)
        super().save(*args, **kwargs)

    def __str__(self):
        """Unicode representation of Expenses."""
        return f"{self.voucher_number} - {self.supplier.business_name}"

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'voucher_number': self.voucher_number,
            'supplier': self.supplier.business_name,
            'product': self.product.name,
            'quantity': float(self.quantity),
            'unit_price': float(self.unit_price),
            'total': float(self.total),
            'category': self.category.name if self.category else None,
            'payment_type': self.payment_type.name,
        }

class Mermas(BaseModels):
    """Model definition for Mermas."""

    # TODO: Define fields here
    date = models.DateField('Fecha de emisión de merma')
    product = models.ForeignKey(Products, on_delete=models.PROTECT)
    quantity = models.DecimalField('Quantity', max_digits=7, decimal_places=2)
    lost_money = models.DecimalField('Dinero perdido', max_digits=14, decimal_places=2, default=0)

    class Meta:
        """Meta definition for Mermas."""
        verbose_name = 'Merma'
        verbose_name_plural = 'Mermas'
        ordering = ['-date']

    def clean(self):
        from django.core.exceptions import ValidationError # type: ignore
        if self.quantity <= 0:
            raise ValidationError("La cantidad debe ser mayor que cero.")

    def save(self, *args, **kwargs):
        self.full_clean()
        # luego tu lógica
        # Si no se pasa lost_money, se calcula automáticamente
        if not self.lost_money:
            self.lost_money = Decimal(self.product.price) * Decimal(self.quantity)
        super().save(*args, **kwargs)

    def __str__(self):
        """Unicode representation of Mermas."""
        return f"Merma de {self.product.code} - {self.product.name}"

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'product': self.product.name,
            'quantity': float(self.quantity),
            'lost_money': float(self.lost_money),
        }