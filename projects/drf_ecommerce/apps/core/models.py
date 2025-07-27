# py
# django
from django.db import models
# drf
# third
from simple_history.models import HistoricalRecords
# own

# Create your models here.

class BaseModels(models.Model):
    """Model definition for BaseModels."""

    # TODO: Define fields here
    is_active = models.BooleanField('Activated/Deactivated', default=True)
    created_at = models.DateTimeField('Created At', auto_now_add=True)
    updated_at = models.DateTimeField('Updated At', auto_now=True)
    deleted_at = models.DateTimeField('Deleted At', auto_now=True, null=True, blank=True)
    historical = HistoricalRecords(user_model='user.Users', inherit=True)
    
    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        """Meta definition for BaseModels."""

        abstract = True
        verbose_name = 'BaseModel'
        verbose_name_plural = 'BaseModels'