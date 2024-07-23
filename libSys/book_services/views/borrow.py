from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import status
from django.db import transaction

from book_services.helper import return_response, find_reservation_by_book_and_customer
from book_services.models import Borrow, Reservation
from user.models import Customer
from book.models import Book

class BorrowViewSet(ViewSet):
    
    def check_if_book_is_reserved_by_customer(self, book_id, customer_id):
        try:
            book = Book.objects.get(id=book_id)
            customer = Customer.objects.get(id=customer_id)
        except (Book.DoesNotExist, Customer.DoesNotExist):
            return False
        
        reservations = Reservation.objects.filter(book=book, customer=customer, active=True)
        return reservations.exists()
        
    def inactivate_reservation(self, reservation_id):
        try:
            reservation = Reservation.objects.get(id=reservation_id)
            reservation.inactivate_reservation()
        except Reservation.DoesNotExist:
            return return_response(None, status.HTTP_404_NOT_FOUND, {'message': 'Reservation not found'})
    
    @action(detail=True, methods=['POST'])
    def do_borrow(self, request):
        try:
            book = Book.objects.get(id=request.data['book_id'])  
            customer = Customer.objects.get(id=request.data['customer_id'])
            initial_date = request.data['initial_date']
            final_date = request.data['final_date']
        except Book.DoesNotExist:
            return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Book not found'})
        except Customer.DoesNotExist:
            return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Customer not found'})
        
        with transaction.atomic():
            if book.status in ['Reserved', 'Borrowed']:
                if book.status == 'Reserved':
                    if self.check_if_book_is_reserved_by_customer(book.id, customer.id):
                        borrow = Borrow.objects.create(book=book, customer=customer, initial_date=initial_date, final_date=final_date)
                        book.borrow_book()
                        reservation = find_reservation_by_book_and_customer(book.id, customer.id)
                        if reservation:
                            self.inactivate_reservation(reservation.id)
                        return return_response(request, status.HTTP_200_OK, {'message': 'Book borrowed', 'borrow_id': borrow.id})
                    return return_response(request, status.HTTP_409_CONFLICT, {'message': 'Book is already reserved by another customer'})
                return return_response(request, status.HTTP_409_CONFLICT, {'message': 'Book is already borrowed'})
            
            borrow = Borrow.objects.create(book=book, customer=customer, initial_date=initial_date, final_date=final_date)
            book.borrow_book()
            return return_response(request, status.HTTP_200_OK, {'message': 'Book borrowed', 'borrow_id': borrow.id})
    
    @action(detail=True, methods=['DELETE'])
    def delete_borrow(self, request, pk=None):
        try:
            borrow = Borrow.objects.get(id=pk)
        except Borrow.DoesNotExist:
            return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Borrow not found'})
        
        borrow.active = False 
        borrow.cancel_borrow()
        borrow.save()
        borrow.delete()
        return return_response(request, status.HTTP_200_OK, {'message': 'Borrow deleted'})
