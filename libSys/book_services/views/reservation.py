from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import status
from django.db import transaction

from book_services.helper import return_response, check_stock
from book_services.models import Reservation

from user.models import Customer
from book.models import Book, Estoque
from fine.models import Fine

class ReservationViewSet(ViewSet):
    
    @action(detail=True, methods=['POST'])
    def do_reservation(self, request):
        try:
            book = Book.objects.get(id=request.data['book_id'])
            customer = Customer.objects.get(id=request.data['customer_id'])
        except Book.DoesNotExist:
            return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Book not found'})
        except Customer.DoesNotExist:
            return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Customer not found'})

        with transaction.atomic():
            fine=Fine.objects.filter(customer=customer)
            if fine.exists():
                return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Customer has a fine to pay'})
            
            if not check_stock(book.id):
                return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Book not available'})
            
            reservation = Reservation.objects.create(book=book, customer=customer)
            
            estoque=Estoque.objects.get(book=book)
            
            estoque.decrement_quantity()
            estoque.set_status()
           
            return return_response(request, status.HTTP_200_OK, {'message': 'Book reserved', 'reservation_id': reservation.id})

    @action(detail=True, methods=['DELETE'])
    def delete_reservation(self, request, pk=None):
        try:
            reservation = Reservation.objects.get(id=pk)
        except Reservation.DoesNotExist:
            return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Reservation not found'})
        
        estoque=Estoque.objects.get(book=reservation.book)
        
        estoque.increment_quantity()
        estoque.set_status()
        reservation.inactivate_reservation()
        reservation.delete()
        return return_response(request, status.HTTP_200_OK, {'message': 'Reservation canceled'})
