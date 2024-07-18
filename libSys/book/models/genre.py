from django.db import models

from book.models.factory_model import FactoryModel

class Genre(FactoryModel):
    name=models.CharField(max_length=50, unique=True)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table='genre'
        verbose_name='Genre'
        verbose_name_plural='Genres'
        ordering=['name']