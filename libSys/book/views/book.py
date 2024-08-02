from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from book.models import Book, Estoque
from book.serializers import BookSerializer
from book.filters import BookFilter  # Importe o filtro aqui

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter  # Adicione o filtro aqui

    def perform_create(self, serializer):
        isbn = serializer.validated_data['isbn']
        
        if Book.objects.filter(isbn=isbn).exists():
            book = Book.objects.get(isbn=isbn)
            estoque = Estoque.objects.filter(book=book).first()
            if estoque:
                estoque.increment_quantity()
                estoque.set_status()
                estoque.save()
                return Response({'detail': 'Quantidade incrementada no estoque.'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Estoque não encontrado para o livro existente.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            book = serializer.save()
            Estoque.objects.create(book=book, quantity=1)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    @action(detail=False, methods=['get'])
    def check_isbn(self, request):
        isbn = request.query_params.get('isbn', None)
        
        if isbn is not None:
            books = Book.objects.filter(isbn=isbn) 
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data)
        
        return Response({'detail': 'ISBN não informado.'}, status=status.HTTP_400_BAD_REQUEST)
