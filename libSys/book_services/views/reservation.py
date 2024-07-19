from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import status

from book_services.helper import return_response
from book_services.models import Reservation

from user.models import Customer
from book.models import Book

class ReservationViewSet(ViewSet):
    
    @action(detail=True, methods=['post'])
    def do_reservation(self, request):
        try:
            book = Book.objects.get(id=request.data['book_id'])
            customer = Customer.objects.get(id=request.data['customer_id'])
        except Book.DoesNotExist:
            return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Book not found'})
        except Customer.DoesNotExist:
            return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Customer not found'})

        if book.status in ['Reserved', 'Borrowed']:
            if book.status == 'Reserved':
                return return_response(request, status.HTTP_409_CONFLICT, {'message': 'Book is already reserved'})
            return return_response(request, status.HTTP_409_CONFLICT, {'message': 'Book is already borrowed'})
        
        reservation = Reservation.objects.create(book=book, customer=customer)
        book.reserve_book()
        
        return return_response(request, status.HTTP_200_OK, {'message': 'Book reserved', 'reservation_id': reservation.id})
