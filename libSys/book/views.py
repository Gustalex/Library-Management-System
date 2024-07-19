from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from book.helper import return_response

from .models import Book, Genre
from .serializers import BookSerializer, GenreSerializer


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    
    
class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    @action(detail=True, methods=['PUT'])
    def change_status_reserve_book(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return return_response(request, 404, {'message': 'Book not found'})
            
        book.reserve_book()
        return return_response(request, 200, {'message': 'Book reserved'})
    
    @action(detail=True, methods=['PUT'])
    def change_status_borrow_book(self, request, pk=None):    
        try:
            book = Book.objects.get(pk=pk)
            if book.book_status in ['Reserved', 'Borrowed']:
                return return_response(request, 409, {'message': 'Book is not available'})
        except Book.DoesNotExist:
            return return_response(request, 404, {'message': 'Book not found'})
        
        book.borrow_book()
        return return_response(request, 200, {'message': 'Book borrowed'})
    
    @action(detail=True, methods=['PUT'])
    def change_status_return_book(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return return_response(request, 404, {'message': 'Book not found'})
        
        book.return_book()
        return return_response(request, 200, {'message': 'Book returned'})     
