from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from book.models import Book, Estoque
from book.serializers import BookSerializer
from book.filters import BookFilter

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter

    def perform_create(self, serializer):
        isbn = serializer.validated_data['isbn']
        
        existing_book = Book.all_objects.filter(isbn=isbn).first()
        
        if existing_book:
            estoque = Estoque.objects.filter(book=existing_book,is_deleted=False).first()
            estoque.increment_quantity()
            estoque.set_status()
            if existing_book.is_deleted:
                estoque = Estoque.objects.filter(book=existing_book).first()
                if estoque:
                    estoque.quantity=1
                    estoque.set_status()
                    estoque.save()
                    existing_book.rollback()
                    return Response({'detail': 'Livro restaurado e quantidade no estoque incrementada.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'detail': 'Estoque não encontrado para o livro existente.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'detail': 'Livro com este ISBN já existe.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            book = serializer.save()
            Estoque.objects.create(book=book, quantity=1)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    @action(detail=False, methods=['get'])
    def check_isbn(self, request):
        isbn = request.query_params.get('isbn', None)
        
        if isbn:
            try:
                books = Book.all_objects.filter(isbn=isbn)
                serializer = BookSerializer(books, many=True)
                return Response(serializer.data)
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'detail': 'ISBN não informado.'}, status=status.HTTP_400_BAD_REQUEST)
