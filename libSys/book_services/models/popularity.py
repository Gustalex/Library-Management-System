from django.db import models

from book_services.models import FactoryModel
from book.models import Book

class Popularity(FactoryModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_count = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'popularity'
        verbose_name = 'Popularity'
        verbose_name_plural = 'Popularities'
        ordering = ['-borrow_count']
        
    def increment_borrow_count(self):
        self.borrow_count += 1
        self.save()
    
    
    