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
        try:
            isbn = serializer.validated_data['isbn']
            existing_book = self._get_existing_book(isbn)
            
            if existing_book:
                self._update_existing_book_stock(existing_book)
            else:
                self._create_new_book_and_stock(serializer)
        except Exception as e:
            return Response({'detail': f'Ocorreu um erro: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _get_existing_book(self, isbn):
        return Book.objects.filter(isbn=isbn).first()

    def _update_existing_book_stock(self, book):
        try:
            estoque = Estoque.objects.filter(book=book).first()
            if estoque:
                estoque.increment_quantity()
                estoque.set_status()
                estoque.save()
            else:
                raise ValueError("Estoque não encontrado para o livro existente.")
        except Exception as e:
            raise ValueError(f"Erro ao atualizar estoque: {str(e)}")

    def _create_new_book_and_stock(self, serializer):
        try:
            book = serializer.save()
            Estoque.objects.create(book=book, quantity=1)
        except Exception as e:
            raise ValueError(f"Erro ao criar novo livro e estoque: {str(e)}")
        
    @action(detail=False, methods=['get'])
    def check_isbn(self, request):
        isbn = request.query_params.get('isbn', None)
        
        if isbn:
            try:
                books = Book.objects.filter(isbn=isbn)
                serializer = BookSerializer(books, many=True)
                return Response(serializer.data)
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'detail': 'ISBN não informado.'}, status=status.HTTP_400_BAD_REQUEST)
