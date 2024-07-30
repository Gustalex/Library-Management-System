from django.db import models
from book.models import Book
from book_services.models import FactoryModel

class Reservation(FactoryModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    customer = models.ForeignKey('user.Customer', on_delete=models.CASCADE, related_name='reservation_set')
    active = models.BooleanField(default=True)
    class Meta:
        db_table = 'reservations'
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'
    
    def inactivate_reservation(self):
        self.active = False
        self.save(update_fields=['active'])