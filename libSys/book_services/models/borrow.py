from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from book.models import Book
from book_services.models import FactoryModel

def validate_date(value):
    if value < timezone.now().date():
        raise ValidationError('Please enter a valid date')
    
class Borrow(FactoryModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    customer = models.ForeignKey('user.Customer', on_delete=models.CASCADE, related_name='borrow_set')
    initial_date = models.DateField()
    final_date = models.DateField(validators=[validate_date])
    active = models.BooleanField(default=True)    
    class Meta:
        db_table = 'borrows'
        verbose_name = 'Borrow'
        verbose_name_plural = 'Borrows'
    
    def clean(self):
        if self.initial_date > self.final_date:
            raise ValidationError('The initial date must be less than the final date')
    
    def cancel_borrow(self):
        self.active = False
        self.save(update_fields=['active'])
        
    def calculate_fine(self):
        if self.active:
            today = timezone.now().date()
            if today > self.final_date:
                days_late = (today - self.final_date).days
                return days_late * 2.0
            return 0
        return 0
