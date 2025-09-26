# py
from decimal import Decimal
# django
from django.db import models # type: ignore
from django.utils import timezone # type: ignore
# drf
# third
# own
from apps.core.models import BaseModels, DiscountTypes

# Create your models here.

class MeasureUnits(BaseModels):
    """Model definition for MeasureUnits."""

    # TODO: Define fields here.
    description = models.CharField('Description', max_length=50, blank=False, null=False, unique=True)

    class Meta:
        """Meta definition for MeasureUnits."""

        verbose_name = 'MeasureUnit'
        verbose_name_plural = 'MeasureUnits'

    def __str__(self):
        """Unicode representation of MeasureUnits."""
        return self.description

class CategoriesProduct(BaseModels):
    """Model definition for CategoriesProduct."""

    # TODO: Define fields here
    description = models.CharField('Description', max_length=50, unique=True, blank=False, null=False)

    class Meta:
        """Meta definition for CategoriesProduct."""

        verbose_name = 'CategoriesProduct'
        verbose_name_plural = 'CategoriesProducts'

    def __str__(self):
        """Unicode representation of CategoriesProduct."""
        return self.description

class Products(BaseModels):
    """Model definition for Products."""
    
    # TODO: Define fields here
    name = models.CharField('Product Name', max_length=150, unique=True, blank=False, null=False)
    description = models.TextField('Product Description', blank=False, null=False)
    measure_unit = models.ForeignKey(MeasureUnits, on_delete=models.CASCADE, verbose_name='Measure Unit', null=True)
    category = models.ForeignKey(CategoriesProduct, on_delete=models.CASCADE, verbose_name='Product Category', null=True)
    image = models.ImageField('Product Image', upload_to='products/', blank=True, null=True)
    
    # Precio de venta real (editable)
    price = models.DecimalField(
        'Sale Price',
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Precio final de venta al cliente."
    )
    
    # Margen sobre el costo (editable)
    profit_percentage = models.DecimalField(
        'Profit (%)',
        max_digits=5,
        decimal_places=2,
        default=30.00,
        help_text="Porcentaje de ganancia sobre el costo."
    )

    class Meta:
        """Meta definition for Products."""

        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        """Unicode representation of Products."""
        return self.name
    
    @property
    def last_price(self):
        """Último costo del producto según Expenses"""
        last_expense = self.expenses.order_by('-created_at').first()
        return last_expense.unit_price if last_expense else self.price
    
    @property
    def suggested_price(self):
        """Precio sugerido con margen (%) aplicado al último costo"""
        if self.last_price:
            return self.last_price * (1 + (self.profit_percentage / 100))
        return self.price
    
    # para llamar como se fuera un propiedad -> example -> product.stock.
    @property
    def stock(self):
        # py
        # django
        from django.db.models import Sum # type: ignore
        # drf
        # third
        # own
        # se pone aca para evitar errores ya que si lo pongo en la parte inicial de este file.py puede caudar un error circular.
        # ya que en en apps.features.expense.models estoy utilizando el Products de este file.py
        from apps.features.expense.models import Expenses, Mermas
        
        # comprados.
        expenses = Expenses.objects.filter(
            product=self,
            is_active=True
        ).aggregate(Sum('quantity'))
        
        # vencidos o perdidos.
        mermas = Mermas.objects.filter(
            product=self,
            is_active=True
        ).aggregate(Sum('quantity'))
        
        # int(entity['quantity__sum'] or 0.00) -> Solo retornas el número, no el diccionario
        stock = (int(expenses['quantity__sum'] or 0.00) - int(mermas['quantity__sum'] or 0.00))

        return stock
    
    @property
    def final_price(self):
        """
        Calcula el precio final:
        1. Aplica promo directa al producto si existe.
        2. Sino, aplica promo de la categoría.
        3. Sino, retorna el precio normal.
        """
        now = timezone.now()

        # --- Promo de producto ---
        promo_product = self.promotions.filter(
            is_active=True,
            start_date__lte=now
        ).filter(
            models.Q(end_date__isnull=True) | models.Q(end_date__gte=now)
        ).order_by('-discount_value').first()

        if promo_product:
            return self._apply_discount(promo_product)

        # --- Promo de categoría ---
        if self.category:
            promo_category = self.category.promotions.filter(
                is_active=True,
                start_date__lte=now
            ).filter(
                models.Q(end_date__isnull=True) | models.Q(end_date__gte=now)
            ).order_by('-discount_value').first()

            if promo_category:
                return self._apply_discount(promo_category)

        # --- Sin promo ---
        return self.price

    def _apply_discount(self, promo):
        """Aplica un descuento según el tipo (PERCENTAGE o AMOUNT)."""
        if promo.discount_type.code == "PERCENTAGE":
            discount_amount = (self.price * promo.discount_value) / Decimal(100)
            return self.price - discount_amount

        elif promo.discount_type.code == "AMOUNT":
            return max(Decimal("0.0"), self.price - promo.discount_value)

        return self.price

class Promotions(BaseModels):
    """Model definition for Promotions."""

    # TODO: Define fields here
    name = models.CharField('Promotion Name', max_length=150)  # Ej: "Promo Navidad 2025"
    description = models.TextField('Promotion Description', blank=True, null=True)

    # Relación con tipo de descuento
    discount_type = models.ForeignKey(
        DiscountTypes,
        on_delete=models.PROTECT,
        related_name="promotions",
        verbose_name="Discount Type"
    )
    discount_value = models.DecimalField(
        'Discount Value',
        max_digits=10,
        decimal_places=2,
        help_text="Porcentaje (%) o monto fijo según DiscountType"
    )

    # Fechas de vigencia
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True, null=True)

    # Aplicación a productos o categorías
    categories = models.ManyToManyField(
        CategoriesProduct,
        related_name="promotions",
        blank=True
    )
    products = models.ManyToManyField(
        Products,
        related_name="promotions",
        blank=True
    )

    class Meta:
        """Meta definition for Promotions."""

        verbose_name = "Promotion"
        verbose_name_plural = "Promotions"

    def __str__(self):
        """Unicode representation of Promotions."""
        return f"{self.name} ({self.discount_type.code}: {self.discount_value})"

    @property
    def is_valid(self):
        """Verifica si la promoción está activa y dentro de fechas"""
        now = timezone.now()
        return (
            self.is_active and
            (self.start_date <= now) and
            (self.end_date is None or self.end_date >= now)
        )