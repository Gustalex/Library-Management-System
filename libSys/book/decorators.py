from functools import wraps
from rest_framework.response import Response 
from rest_framework import status 
from book.models import Book 

def validade_book_exists(func):
    @wraps(func)
    def wrapper(self, request, pk=None, *args, **kwargs):
        try:
            book=Book.objects.get(pk=pk)
            return func(self, request, book, *args, **kwargs)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
    return wrapper

def validate_cover_image(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        cover_image=request.FILES.get('cover_image')
        if not cover_image:
            return Response({'error': 'No cover image provided'}, status=status.HTTP_400_BAD_REQUEST)
        return func(self, request, cover_image=cover_image, *args, **kwargs)
    return wrapper
        