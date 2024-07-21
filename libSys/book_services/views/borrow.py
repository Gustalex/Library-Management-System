from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import status

from book_services.helper import return_response
from book_services.models import (Borrow, Reservation)

from user.models import Customer
from book.models import Book


class BorrowViewSet(ViewSet):
    
    def check_if_book_is_reserved_by_customer(self, book, customer):
        book=Book.objects.get(id=book)
        customer=Customer.objects.get(id=customer)
        
        reservations = Reservation.objects.filter(book=book, customer=customer, is_deleted=False)
        if reservations:
            return True
        return False
    
    def find_reservation_by_book_and_customer(self, book_id, customer_id):
        try:
            book = Book.objects.get(id=book_id)
            customer = Customer.objects.get(id=customer_id)
        except (Book.DoesNotExist, Customer.DoesNotExist):
            return None
        
        reservation = Reservation.objects.filter(book=book, customer=customer, is_deleted=False).first()
        return reservation
            
    def delete_reservation(self, reservation_id):
        try:
            reservation = Reservation.objects.get(id=reservation_id)
        except Reservation.DoesNotExist:
            return None
        
        reservation.delete()
    
    @action(detail=True, methods=['POST'])
    def do_borrow(self,request):
        try:
            book=Book.objects.get(id=request.data['book_id'])  
            customer=Customer.objects.get(id=request.data['customer_id'])
            initial_date=request.data['initial_date']
            final_date=request.data['final_date']
            
        except Book.DoesNotExist:
            return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Book not found'})
        except Customer.DoesNotExist:
            return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Customer not found'})
        
        if book.status in ['Reserved', 'Borrowed']:
            if book.status == 'Reserved':
                if(self.check_if_book_is_reserved_by_customer(book.id, customer.id)):
                    borrow = Borrow.objects.create(book=book, customer=customer, initial_date=initial_date, final_date=final_date)
                    book.borrow_book()
                    reservation = self.find_reservation_by_book_and_customer(book.id, customer.id)
                    self.delete_reservation(reservation.id)
                                    
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
        
        borrow.cancel_borrow()
        
        return return_response(request, status.HTTP_200_OK, {'message': 'Borrow deleted'})