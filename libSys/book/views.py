from rest_framework.viewsets import ModelViewSet

from book.helper import *

from .models import *
from .serializers import *



class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    
    def partial_update(self, request, pk=None):
        try:
            genre = Genre.objects.get(pk=pk)
        except:
            return return_response(request, 404, {'message': 'Genre not found'})
        
        serializer = GenreSerializer(genre, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return return_response(request, 200, serializer.data)
        
        return return_response(request, 400, serializer.errors)
    
class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def partial_update(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
        except:
            return return_response(request, 404, {'message': 'Book not found'})
        
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return return_response(request, 200, serializer.data)
        
        return return_response(request, 400, serializer.errors)
    
    def reserve_book(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
            
        except:
            return return_response(request, 404, {'message': 'Book not found'})
            
        book.reserve_book()
        return return_response(request, 200, {'message': 'Book reserved'})
    
    def borrow_book(self, request, pk=None):    
        try:
            book = Book.objects.get(pk=pk)
            
            if book.book_status == 'Reserved' or book.book_status == 'Borrowed':
                return return_response(request, 409, {'message': 'Book is not avaliable'})
            
        except:
            return return_response(request, 404, {'message': 'Book not found'})
        
        book.borrow_book()
        return return_response(request, 200, {'message': 'Book borrowed'})
    
    def return_book(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
        except:
            return return_response(request, 404, {'message': 'Book not found'})
        
        book.return_book()
        return return_response(request, 200, {'message': 'Book returned'})     
    
    def borrow_reserved_book(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
            
            if book.book_status == 'Reserved':
                book.borrow_book()
                return return_response(request, 200, {'message': 'Book borrowed'})
            
            return return_response(request, 400, {'message': 'Book is not reserved'})
        
        except:
            return return_response(request, 404, {'message': 'Book not found'})
        
        

    
    
    