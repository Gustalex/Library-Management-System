from django.db import models

from book.models.factory_model import FactoryModel
from book.models.genre import Genre

class Book(FactoryModel):
    title=models.CharField(max_length=100)
    author=models.CharField(max_length=50)
    id_genre=models.ForeignKey(Genre, on_delete=models.CASCADE)
    book_status=models.CharField(max_length=30, default='Avaliable')
    
    def reserve_book(self):
        self.book_status='Reserved'
        self.save()
    
    def borrow_book(self):
        self.book_status='Borrowed'
        self.save()
    
    def return_book(self):
        self.book_status='Avaliable'
        self.save()
    
    def __str__(self) -> str: 
        return self.title
    
    class Meta:
        db_table='book'
        verbose_name='Book'
        verbose_name_plural='Books'
        ordering=['title']