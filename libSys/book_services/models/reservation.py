from django.db import models
from book.models import Book
from book_services.models import FactoryModel

class Reservation(FactoryModel):
    id_book = models.ForeignKey(Book, on_delete=models.CASCADE)
    id_customer = models.ForeignKey('user.Customer', on_delete=models.CASCADE, related_name='reservation_set')
    
    class Meta:
        db_table = 'reservations'
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'
        
    def cancel_reservation(self):
        book = self.id_book
        book.return_book()
        self.delete()
