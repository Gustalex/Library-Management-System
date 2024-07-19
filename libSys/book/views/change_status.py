from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import status

from book.helper import return_response
from book.models import Book
from book.serializers import UpdateStatusSerializer

class UpdateStatusBookViewSet(ViewSet):
    queryset = Book.objects.all()
    serializer_class = UpdateStatusSerializer

    @action(detail=True, methods=['PUT'])
    def change_status_reserve_book(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Book not found'})

        book.reserve_book()
        return return_response(request, status.HTTP_200_OK, {'message': 'Book reserved'})

    @action(detail=True, methods=['PUT'])
    def change_status_borrow_book(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
            if book.book_status in ['Reserved', 'Borrowed']:
                return return_response(request, status.HTTP_409_CONFLICT, {'message': 'Book is not available'})
        except Book.DoesNotExist:
            return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Book not found'})

        book.borrow_book()
        return return_response(request, status.HTTP_200_OK, {'message': 'Book borrowed'})

    @action(detail=True, methods=['PUT'])
    def change_status_return_book(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Book not found'})

        book.return_book()
        return return_response(request, status.HTTP_200_OK, {'message': 'Book returned'})