# py
# django
from django.db import models
# drf
# third
# own
from apps.core.models import BaseModels

# Create your models here.

class Countries(BaseModels):
    """Model definition for Countries."""

    # TODO: Define fields here
    code = models.CharField('Country Code', max_length=3, unique=True) # Ej: "COL", "USA"
    name = models.CharField('Country Name', max_length=100) # Ej: "Colombia", "Estados Unidos"

    class Meta:
        """Meta definition for Countries."""
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ['code']

    def __str__(self):
        """Unicode representation of Countries."""
        return f"{self.code} - {self.name}"

class Cities(BaseModels):
    """Model definition for Cities."""

    # TODO: Define fields here
    code = models.CharField('City Code', max_length=10, unique=True)
    name = models.CharField('City Name', max_length=100)
    country = models.ForeignKey(Countries, on_delete=models.PROTECT, related_name="cities", verbose_name="Country")

    class Meta:
        """Meta definition for Cities."""

        verbose_name = 'City'
        verbose_name_plural = 'Cities'
        ordering = ['code']

    def __str__(self):
        """Unicode representation of Cities."""
        return f"{self.code} - {self.name}, {self.country.code}"
