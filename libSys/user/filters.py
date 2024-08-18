import django_filters
from user.models import Customer

class CustomerFilter(django_filters.FilterSet):
    cpf = django_filters.CharFilter(lookup_expr='icontains')
    name = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Customer
        fields = ['cpf', 'name']