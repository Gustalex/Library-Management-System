from rest_framework.viewsets import ModelViewSet

from event.serializers import EventSerializer
from event.models import Event

from django_filters.rest_framework import DjangoFilterBackend
from event.filters import EventFilter

class EventViewSet(ModelViewSet):
    queryset=Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter
