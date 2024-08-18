import django_filters
from book_services.models import Borrow, Reservation
from user.models import Customer

class BorrowFilter(django_filters.FilterSet):
    customer_name = django_filters.CharFilter(field_name='customer__name', lookup_expr='icontains')
    customer_cpf = django_filters.CharFilter(field_name='customer__cpf', lookup_expr='icontains')
    
    class Meta:
        model = Borrow
        fields = ['customer_name', 'customer_cpf']


class ReservationFilter(django_filters.FilterSet):
    customer_name = django_filters.CharFilter(field_name='customer__name', lookup_expr='icontains')
    customer_cpf = django_filters.CharFilter(field_name='customer__cpf', lookup_expr='icontains')
    
    class Meta:
        model = Reservation
        fields = ['customer_name', 'customer_cpf']
    