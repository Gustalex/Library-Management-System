from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from .factory_model import FactoryModel

def validate_date(value):
    if value < timezone.now().date():
        raise ValidationError('Please enter a valid date')
    
class Event(FactoryModel):
    name = models.CharField(max_length=50)
    date = models.DateField()
    
    class Meta:
        db_table = 'events'
        verbose_name = 'Event'
        verbose_name_plural='Events'