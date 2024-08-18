import django_filters
from fine.models import Fine
from user.models import Customer

class FineFilter(django_filters.FilterSet):
    customer_name = django_filters.CharFilter(field_name='customer__name', lookup_expr='icontains')
    customer_cpf = django_filters.CharFilter(field_name='customer__cpf', lookup_expr='icontains')
    
    class Meta:
        model = Fine
        fields = ['customer_name', 'customer_cpf']