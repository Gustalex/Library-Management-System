from django.db import models

from book.models.factory_model import FactoryModel
from book.models.genre import Genre

class Book(FactoryModel):
    isbn=models.CharField(max_length=20, unique=True, blank=True, null=True)
    title=models.CharField(max_length=100)
    author=models.CharField(max_length=50)
    genre=models.ForeignKey(Genre, on_delete=models.CASCADE)
    edition=models.CharField(max_length=50, blank=True, null=True)
    synopsis=models.TextField(blank=True, null=True) 
    
    def __str__(self) -> str: 
        return self.title
    
    class Meta:
        db_table='book'
        verbose_name='Book'
        verbose_name_plural='Books'
        ordering=['title']