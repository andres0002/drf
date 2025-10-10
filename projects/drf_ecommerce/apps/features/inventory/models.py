# py
# django
from django.db import models # type: ignore
from django.db import transaction # type: ignore
# drf
# third
# own
from apps.core.models import BaseModels, MovementTypes
from apps.features.product.models import Products
from apps.features.expense.models import Expenses
from apps.features.sale.models import Sales

# Create your models here.

class Warehouses(BaseModels):
    """Model definition for Warehouses."""

    # TODO: Define fields here
    code = models.CharField(
        'Code',
        max_length=20,
        unique=True,
        help_text="Código corto para identificar la bodega (ej: BOG-CENTRAL)"
    )
    name = models.CharField(
        'Name',
        max_length=150,
        help_text="Nombre descriptivo de la bodega (ej: Bodega Central Bogotá)"
    )
    address = models.CharField(
        'Address',
        max_length=255,
        null=True, blank=True
    )
    country = models.ForeignKey(
        'shared.Countries',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='warehouses',
        verbose_name='Country'
    )
    city = models.ForeignKey(
        'shared.Cities',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='warehouses',
        verbose_name='City'
    )
    user = models.ForeignKey(
        'user.Users',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='warehouses',
        verbose_name='User'
    )
    notes = models.TextField(null=True, blank=True)

    class Meta:
        """Meta definition for Warehouses."""
        verbose_name = 'Warehouse'
        verbose_name_plural = 'Warehouses'
        ordering = ['id']

    def __str__(self):
        """Unicode representation of Warehouses."""
        return f"{self.code} - {self.name}"

class Stocks(BaseModels):
    """Model definition for Stocks."""

    # TODO: Define fields here
    product = models.ForeignKey(
        Products,
        on_delete=models.PROTECT,
        related_name="stocks",
        verbose_name='Product'
    )
    warehouse = models.ForeignKey(
        Warehouses,
        on_delete=models.PROTECT,
        related_name="stocks",
        verbose_name="Warehouse"
    )
    quantity = models.IntegerField('Quantity', default=0, help_text="Cantidad actual en stock físico")

    class Meta:
        """Meta definition for Stocks."""
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'
        unique_together = ('product', 'warehouse')  # Cada producto solo una vez por bodega
        ordering = ['warehouse', 'product']

    def __str__(self):
        """Unicode representation of Stocks."""
        return f"{self.product.name} - {self.quantity} en {self.warehouse.name}"

    def to_dict(self):
        """Conversión rápida a dict para auditoría o respuesta API."""
        return {
            'product_id': self.product.id,
            'product_name': self.product.name,
            'warehouse': self.warehouse.name,
            'quantity': self.quantity,
            'updated_at': self.updated_at.isoformat()
        }

class InventoryMovements(BaseModels):
    """Model definition for InventoryMovements."""

    # TODO: Define fields here
    product = models.ForeignKey(
        Products,
        on_delete=models.PROTECT,
        related_name="inventory_movements",
        verbose_name='Product'
    )
    warehouse = models.ForeignKey(
        Warehouses,
        on_delete=models.PROTECT,
        related_name="inventory_movements",
        verbose_name="Warehouse"
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
    balance = models.IntegerField('Balance', default=0, help_text="Saldo resultante después del movimiento", editable=False)
    notes = models.TextField('Notes', null=True, blank=True, help_text="Notas o comentarios del movimiento.")

    class Meta:
        """Meta definition for InventoryMovements."""
        verbose_name = 'Inventory Movement'
        verbose_name_plural = 'Inventory Movements'
        ordering = ['-created_at']

    def __str__(self):
        """Unicode representation of InventoryMovements."""
        return f"{self.product.name} - {self.movement_type.name} ({self.quantity})"

    @transaction.atomic
    def save(self, *args, **kwargs):
        """
        Calcula y actualiza el stock del producto automáticamente según el tipo de movimiento - Evita dobles guardados recursivos.
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
            stock, _ = Stocks.objects.get_or_create(product=self.product, warehouse=self.warehouse)
            new_quantity = stock.quantity + self.quantity

            # Evitar que el stock quede negativo
            if new_quantity < 0:
                raise ValueError(
                    f"Stock insuficiente en {self.warehouse.name} para {self.product.name}."
                    f"Actual: {stock.quantity}, movimiento: {self.quantity}"
                )
            
            stock.quantity = new_quantity
            stock.save(update_fields=['quantity', 'updated_at'])

            # Actualizar balance del movimiento con el nuevo stock
            self.balance = stock.quantity
            super().save(update_fields=['balance', 'updated_at'])

class WarehouseTransfers(BaseModels):
    """Model definition for WarehouseTransfers."""

    # TODO: Define fields here
    product = models.ForeignKey(
        Products,
        on_delete=models.PROTECT,
        related_name="warehouse_transfers",
        verbose_name="Product"
    )
    origin = models.ForeignKey(
        Warehouses,
        on_delete=models.PROTECT,
        related_name="transfers_out",
        verbose_name="Origin Warehouse"
    )
    destination = models.ForeignKey(
        Warehouses,
        on_delete=models.PROTECT,
        related_name="transfers_in",
        verbose_name="Destination Warehouse"
    )
    quantity = models.PositiveIntegerField(help_text="Cantidad a transferir")
    notes = models.TextField(null=True, blank=True)

    class Meta:
        """Meta definition for WarehouseTransfers."""
        verbose_name = 'Warehouse Transfer'
        verbose_name_plural = 'Warehouse Transfers'
        ordering = ['-created_at']

    def __str__(self):
        """Unicode representation of WarehouseTransfers."""
        return f"Transferencia {self.quantity} {self.product.name} de {self.origin.code} a {self.destination.code}"
    
    @transaction.atomic
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            # Crear movimiento de salida en origen
            InventoryMovements.objects.create(
                product=self.product,
                warehouse=self.origin,
                movement_type=MovementTypes.objects.get(code='OUT'),
                quantity=-self.quantity,
                notes=f"Transferencia hacia {self.destination.name}"
            )

            # Crear movimiento de entrada en destino
            InventoryMovements.objects.create(
                product=self.product,
                warehouse=self.destination,
                movement_type=MovementTypes.objects.get(code='IN'),
                quantity=self.quantity,
                notes=f"Transferencia desde {self.origin.name}"
            )