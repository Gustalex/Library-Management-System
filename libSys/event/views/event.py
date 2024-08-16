from rest_framework.viewsets import ModelViewSet

from event.serializers import EventSerializer
from event.models import Event


class EventViewSet(ModelViewSet):
    queryset=Event.objects.all()
    serializer_class = EventSerializer

