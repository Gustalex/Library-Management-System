from django.db import models

from book.models.factory_model import FactoryModel
from book.models.book import Book


class Estoque(FactoryModel):
    book=models.ForeignKey(Book, on_delete=models.CASCADE, related_name='estoques')
    quantity=models.IntegerField()
    status=models.CharField(max_length=20, default='Last Unit')
    
    class Meta:
        db_table='estoque'
        verbose_name='Estoque'
        verbose_name_plural='Estoques'
        ordering=['book']
    
    def increment_quantity(self):
        self.quantity+=1
        self.save(update_fields=['quantity'])
        
    def decrement_quantity(self):
        self.quantity-=1
        self.save(update_fields=['quantity'])
        
    def set_status(self):
        if self.quantity>1:
            self.status='Available'
        elif self.quantity==1:
            self.status='Last Unit'
        else:
            self.status='Unavailable'
        self.save(update_fields=['status'])
    
    def __str__(self) -> str:
        return f'{self.book} - {self.quantity}'
        