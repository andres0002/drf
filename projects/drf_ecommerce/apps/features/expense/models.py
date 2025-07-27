# py
# django
from django.db import models
# drf
# third
# own
from apps.core.models import BaseModels
from apps.features.product.models import Products

# Create your models here.

class Suppliers(BaseModels):
    """Model definition for Suppliers."""

    # TODO: Define fields here
    ruc = models.CharField(unique=True, max_length=11)
    business_name = models.CharField('Comapny Name', max_length=150, null=False, blank=False)
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
        return self.business_name
    
    def to_dict(self):
        return {
            'id': self.id,
            'ruc': self.ruc,
            'business_name': self.business_name,
            'address': self.address,
            'phone': self.phone,
            'email': self.email
        }

class PaymentTypes(BaseModels):
    """Model definition for PaymentTypes."""

    # TODO: Define fields here
    name = models.CharField('Payment Type Name', max_length=100)

    class Meta:
        """Meta definition for PaymentTypes."""

        verbose_name = 'Payment Type'
        verbose_name_plural = 'Payment Types'
        ordering = ['id']

    def __str__(self):
        """Unicode representation of PaymentTypes."""
        return self.name

class Vouchers(BaseModels):
    """Model definition for Vouchers."""

    # TODO: Define fields here
    name = models.CharField('Payment Voucher Name', max_length=100)

    class Meta:
        """Meta definition for Vouchers."""

        verbose_name = 'Voucher'
        verbose_name_plural = 'Vouchers'
        ordering = ['id']

    def __str__(self):
        """Unicode representation of Vouchers."""
        return self.name

class CategoriesExpense(BaseModels):
    """Model definition for CategoriesExpense."""

    # TODO: Define fields here
    name = models.CharField('Categories Expense Name', max_length=100)

    class Meta:
        """Meta definition for CategoriesExpense."""

        verbose_name = 'Category Expense'
        verbose_name_plural = 'Categories Expense'
        ordering = ['id']

    def __str__(self):
        """Unicode representation of CategoriesExpense."""
        return self.name

class Expenses(BaseModels):
    """Model definition for Expenses."""

    # TODO: Define fields here
    date = models.DateField('Fecha de Emisión de Factura', auto_now=False, auto_now_add=False)
    quantity = models.DecimalField('Quantity', max_digits=10, decimal_places=2)
    unit_price = models.DecimalField('Precio Unitario', max_digits=10, decimal_places=2, default=0)
    voucher_number = models.CharField('Número de Comprobante', max_length=50)
    total = models.DecimalField('Total', max_digits=10, decimal_places=2, default=0)
    voucher = models.ForeignKey(Vouchers, on_delete=models.CASCADE)
    user = models.ForeignKey('user.Users', on_delete=models.CASCADE)
    supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
    payment_type = models.ForeignKey(PaymentTypes, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    category = models.ForeignKey(CategoriesExpense, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        """Meta definition for Expenses."""

        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'
        ordering = ['id']

    def __str__(self):
        """Unicode representation of Expenses."""
        return self.voucher_number

class Mermas(BaseModels):
    """Model definition for Mermas."""

    # TODO: Define fields here
    date = models.DateField('Fecha de emisión de merma', auto_now=False, auto_now_add=False)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.DecimalField('Quantity', max_digits=7, decimal_places=2)
    lost_modey = models.DecimalField('Dinero perdido', max_digits=10, decimal_places=2, default=0)

    class Meta:
        """Meta definition for Mermas."""

        verbose_name = 'Merma'
        verbose_name_plural = 'Mermas'
        ordering = ['id']

    def __str__(self):
        """Unicode representation of Mermas."""
        return f"Merma de {self.product.__str__()}"