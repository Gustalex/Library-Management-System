from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import status
from django.db import transaction
from book_services.helper import return_response, find_reservation_by_book_and_customer
from book_services.models import Borrow, Reservation, Popularity
from user.models import Customer
from book.models import Book, Estoque

class BorrowViewSet(ViewSet):
    
    def check_stock(self, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return False
        
        estoque = Estoque.objects.filter(book=book, quantity__gt=0, status__in=['Available', 'Last Unit'])
        return estoque.exists()

    def update_popularity_by_book_id(self, book_id):
        book = Book.objects.get(id=book_id)
        popularity, created = Popularity.objects.get_or_create(book=book)
        popularity.increment_borrow_count()
    
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
            if self.check_stock(book.id):
                estoque = Estoque.objects.filter(book=book, quantity__gt=0, status__in=['Available', 'Last Unit']).first()
                borrow = Borrow.objects.create(book=book, customer=customer, initial_date=initial_date, final_date=final_date)
                self.update_popularity_by_book_id(book.id)
                estoque.decrement_quantity()
                estoque.set_status()
                estoque.save()
                reservation = find_reservation_by_book_and_customer(book.id, customer.id)
                if reservation:
                    self.inactivate_reservation(reservation.id)
                return return_response(request, status.HTTP_201_CREATED, {'message': 'Book borrowed successfully'})
            else:
                return return_response(request, status.HTTP_400_BAD_REQUEST, {'message': 'Book not available'})
                
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
