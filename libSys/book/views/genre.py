from rest_framework.viewsets import ModelViewSet

from book.models import Genre
from book.serializers import GenreSerializer

class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer