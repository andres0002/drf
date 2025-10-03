# py
# django
from django.db import models # type: ignore
# drf
# third
# own
from apps.core.models import BaseModels, MovementTypes
from apps.features.product.models import Products
from apps.features.expense.models import Expenses
from apps.features.sale.models import Sales

# Create your models here.

class InventoryMovements(BaseModels):
    """Model definition for InventoryMovements."""

    # TODO: Define fields here
    product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        related_name="inventory_movements"
    )
    movement_type = models.ForeignKey(
        MovementTypes,
        on_delete=models.PROTECT,
        related_name="inventory_movements"
    )
    reference_sale = models.ForeignKey(
        Sales,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="inventory_movements"
    )
    reference_expense = models.ForeignKey(
        Expenses,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="inventory_movements"
    )
    quantity = models.IntegerField(help_text="Cantidad del movimiento, puede ser positiva (IN) o negativa (OUT)")
    balance = models.IntegerField(default=0, help_text="Saldo resultante después del movimiento")
    notes = models.TextField(null=True, blank=True)

    class Meta:
        """Meta definition for InventoryMovements."""

        verbose_name = 'Inventory Movement'
        verbose_name_plural = 'Inventory Movements'

    def __str__(self):
        """Unicode representation of InventoryMovements."""
        return f"{self.product.name} - {self.movement_type.name} ({self.quantity})"


class Stocks(BaseModels):
    """Model definition for Stocks."""

    # TODO: Define fields here
    product = models.OneToOneField(
        Products,
        on_delete=models.CASCADE,
        related_name="stock"
    )
    quantity = models.IntegerField(default=0, help_text="Cantidad actual en stock físico")

    class Meta:
        """Meta definition for Stocks."""

        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'
        ordering = ['id']

    def __str__(self):
        """Unicode representation of Stocks."""
        return f"{self.product.name} - {self.quantity} en stock"