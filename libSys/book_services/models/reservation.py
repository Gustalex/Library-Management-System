from django.db import models

from models import FactoryModel
from book.models import Book

class Reservation(FactoryModel):
    id_book = models.ForeignKey(Book, on_delete=models.CASCADE)
    #aqui colocar o campo de user quando o modelo user for feito
    
    class Meta:
        db_table = 'reservations'
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'
        
    def cancel_reservation(self):
        book = self.id_book
        book.return_book
        self.delete()


            