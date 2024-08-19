import django_filters
from .models import Event

class EventFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    date = django_filters.DateFilter(field_name='date', lookup_expr='exact')

    class Meta:
        model = Event
        fields = ['name', 'description', 'date']