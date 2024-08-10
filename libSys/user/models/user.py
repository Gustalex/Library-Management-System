from django.db import models
from user.models import FactoryModel

class BaseUser(FactoryModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=14, unique=True)

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.name
    

class Customer(BaseUser):
    reservations = models.ManyToManyField('book_services.Reservation', blank=True, related_name='customers_reservations')
    borrows = models.ManyToManyField('book_services.Borrow', blank=True, related_name='customers_borrows')
    fines = models.ManyToManyField('fine.Fine', blank=True, related_name='customers_fines')    
    class Meta:
        db_table = 'customers'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
