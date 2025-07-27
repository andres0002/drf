# py
# django
from django.db import models
# drf
# third
# own
from apps.core.models import BaseModels

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

class Indicators(BaseModels):
    """Model definition for Indicators."""

    # TODO: Define fields here
    descount_value = models.PositiveSmallIntegerField(default=0)
    category = models.ForeignKey(CategoriesProduct, on_delete=models.CASCADE, verbose_name='Product Category', null=True)

    class Meta:
        """Meta definition for Indicators."""

        verbose_name = 'Indicator'
        verbose_name_plural = 'Indicators'

    def __str__(self):
        """Unicode representation of Indicators."""
        return f'Offer category: {self.category_product}, descount value: {self.descount_value}.'

class Products(BaseModels):
    """Model definition for Products."""
    
    # TODO: Define fields here
    name = models.CharField('Product Name', max_length=150, unique=True, blank=False, null=False)
    description = models.TextField('Product Description', blank=False, null=False)
    measure_unit = models.ForeignKey(MeasureUnits, on_delete=models.CASCADE, verbose_name='Measure Unit', null=True)
    category = models.ForeignKey(CategoriesProduct, on_delete=models.CASCADE, verbose_name='Product Category', null=True)
    image = models.ImageField('Product Image', upload_to='products/', blank=True, null=True)

    class Meta:
        """Meta definition for Products."""

        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        """Unicode representation of Products."""
        return self.name
    
    # para llamar como se fuera un propiedad -> example -> product.stock.
    @property
    def stock(self):
        # py
        # django
        from django.db.models import Sum
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