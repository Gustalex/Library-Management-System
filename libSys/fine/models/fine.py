from django.db import models
from .factory_model import FactoryModel
from user.models import Customer
from book_services.models import Borrow

class Fine(FactoryModel):
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    borrow=models.ForeignKey(Borrow, on_delete=models.CASCADE)
    value=models.FloatField()
    status=models.BooleanField(default=True)
    
    class Meta:
        db_table='fine'
        verbose_name='Fine'
        verbose_name_plural='Fines'
    
    def conclude_fine(self):
        self.status=False
        self.save(update_fields=['status'])
    
    