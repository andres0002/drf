# py
# django
from django.db import models # type: ignore
# drf
# third
# own
from apps.core.models import BaseModels
from apps.features.user.models import Users
from apps.features.product.models import Products

# Create your models here.

class Carts(BaseModels):
    """Model definition for Carts."""
    
    STATUS_CHOICES = (
        ('OPEN', 'Open'),                # Carrito activo en uso
        ('CHECKED_OUT', 'Checked Out'),  # Convertido en venta/pedido
        ('ABANDONED', 'Abandoned'),      # El cliente no lo finalizó
    )

    # TODO: Define fields here
    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name="carts"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='OPEN'
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        """Meta definition for Carts."""

        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
        ordering = ['id']

    def __str__(self):
        """Unicode representation of Carts."""
        return f"Cart {self.id} - {self.user.username} ({self.get_status_display()})"

class CartItems(BaseModels):
    """Model definition for CartItems."""

    # TODO: Define fields here
    cart = models.ForeignKey(
        Carts,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)   # Precio unitario en el momento de agregar
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        """Meta definition for CartItems."""

        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        ordering = ['id']
        unique_together = ('cart', 'product')

    def __str__(self):
        """Unicode representation of CartItems."""
        return f"{self.product.name} x{self.quantity} in Cart {self.cart.id}"
