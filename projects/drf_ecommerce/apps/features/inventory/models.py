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
        on_delete=models.PROTECT,
        related_name="inventory_movements",
        verbose_name='Product'
    )
    movement_type = models.ForeignKey(
        MovementTypes,
        on_delete=models.PROTECT,
        related_name="inventory_movements",
        verbose_name='Movement Type'
    )
    sale = models.ForeignKey(
        Sales,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="inventory_movements",
        verbose_name='Sale'
    )
    expense = models.ForeignKey(
        Expenses,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="inventory_movements",
        verbose_name='Expense'
    )
    quantity = models.IntegerField('Quantity', help_text="Cantidad del movimiento, puede ser positiva (IN) o negativa (OUT)")
    balance = models.IntegerField('Balance', default=0, help_text="Saldo resultante después del movimiento")
    notes = models.TextField('Notes', null=True, blank=True, help_text="Notas o comentarios del movimiento.")

    class Meta:
        """Meta definition for InventoryMovements."""
        verbose_name = 'Inventory Movement'
        verbose_name_plural = 'Inventory Movements'
        ordering = ['-created_at']

    def __str__(self):
        """Unicode representation of InventoryMovements."""
        return f"{self.product.name} - {self.movement_type.name} ({self.quantity})"

    def save(self, *args, **kwargs):
        """
        Calcula y actualiza el stock del producto automáticamente según el tipo de movimiento.
        Evita dobles guardados recursivos.
        Los tipos de movimiento se definen en MovementTypes.code:
        - IN: entrada (suma al stock)
        - OUT: salida (resta del stock)
        - ADJ: ajuste (suma o resta según el valor de quantity)
        """
        is_new = self.pk is None  # Detecta si es un movimiento nuevo
        movement_code = (self.movement_type.code or '').upper()
        
        # Validación básica
        if movement_code not in ['IN', 'OUT', 'ADJ']:
            raise ValueError(f"Tipo de movimiento inválido: {movement_code}")
        
        # Normalizar cantidad según el tipo
        if movement_code == 'IN':
            self.quantity = abs(self.quantity)
        elif movement_code == 'OUT':
            self.quantity = -abs(self.quantity)
        # ADJ mantiene el signo que venga (positivo o negativo)

        super().save(*args, **kwargs)

        # Solo actualizar stock y balance si es nuevo (no actualización de registro)
        if is_new:
            stock, _ = Stocks.objects.get_or_create(product=self.product)
            new_quantity = stock.quantity + self.quantity

            # Evitar que el stock quede negativo
            if new_quantity < 0:
                raise ValueError(
                    f"Stock insuficiente para {self.product.name}. "
                    f"Actual: {stock.quantity}, movimiento: {self.quantity}"
                )
            
            stock.quantity = new_quantity
            stock.save(update_fields=['quantity', 'updated_at'])

            # Actualizar balance del movimiento con el nuevo stock
            self.balance = stock.quantity
            super().save(update_fields=['balance', 'updated_at'])

class Stocks(BaseModels):
    """Model definition for Stocks."""

    # TODO: Define fields here
    product = models.OneToOneField(
        Products,
        on_delete=models.CASCADE,
        related_name="stocks",
        verbose_name='Product'
    )
    quantity = models.IntegerField('Quantity', default=0, help_text="Cantidad actual en stock físico")

    class Meta:
        """Meta definition for Stocks."""

        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'
        ordering = ['id']

    def __str__(self):
        """Unicode representation of Stocks."""
        return f"{self.product.name} - {self.quantity} en stock"

    def to_dict(self):
        """Conversión rápida a dict para auditoría o respuesta API."""
        return {
            'product_id': self.product.id,
            'product_name': self.product.name,
            'quantity': self.quantity,
            'updated_at': self.updated_at.isoformat()
        }