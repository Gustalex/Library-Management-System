from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from models import FactoryModel
from book.models import Book


def validate_date(value):
    if value < timezone.now().date():
        raise ValidationError('Please enter a valid date')
    

class Borrow(FactoryModel):
    id_book=models.ForeignKey(Book, on_delete=models.CASCADE)
    #aqui colocar o campo de user quando o modelo user for feito
    initial_date=models.DateField()
    final_date=models.DateField(validators=[validate_date])
    
    
    class Meta:
        db_table='borrows'
        verbose_name='Borrow'
        verbose_name_plural='Borrows'
    
    
    def clean(self):
        if self.initial_date > self.final_date:
            raise ValidationError('The initial date must be less than the final date')
    
    def cancel_borrow(self):
        book=self.id_book
        book.return_book()
        self.delete()
    
    
    
    