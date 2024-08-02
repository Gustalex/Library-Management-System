from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from book.models import Estoque
from book.serializers import EstoqueSerializer

class EstoqueViewSet(ModelViewSet):
    queryset = Estoque.objects.all()
    serializer_class = EstoqueSerializer

    @action(detail=False, methods=['get'], url_path='by-book/(?P<book_id>[^/.]+)')
    def get_by_book(self, request, book_id=None):
        try:
            estoque = Estoque.objects.filter(book__id=book_id).first()
            if estoque:
                serializer = EstoqueSerializer(estoque)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'detail': 'Stock not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
