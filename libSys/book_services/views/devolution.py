from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import status
from django.db import transaction

from book_services.helper import return_response
from book_services.models import Borrow
from user.models import Customer
from book.models import Book, Estoque

class DevolutionViewSet(ViewSet):

    def _find_borrow_by_book_and_customer(self, book_id, customer_id):
        try:
            book = Book.objects.get(id=book_id)
            customer = Customer.objects.get(id=customer_id)
        except (Book.DoesNotExist, Customer.DoesNotExist):
            return None
        
        return Borrow.objects.filter(book=book, customer=customer, active=True).first()
    
    def _conclude_borrow(self, borrow_id):
        try:
            borrow = Borrow.objects.get(id=borrow_id)
        except Borrow.DoesNotExist:
            return None
        
        borrow.cancel_borrow()
        return borrow

    @action(detail=True, methods=['PATCH'])
    def do_devolution(self, request):
        book_id = request.data.get('book_id')
        customer_id = request.data.get('customer_id')
        
        if not book_id or not customer_id:
            return return_response(request, status.HTTP_400_BAD_REQUEST, {'message': 'Missing parameters'})
        
        try:
            book = Book.objects.get(id=book_id)
            customer = Customer.objects.get(id=customer_id)
        except Book.DoesNotExist:
            return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Book not found'})
        except Customer.DoesNotExist:
            return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Customer not found'})
        
        with transaction.atomic():
            borrow = self._find_borrow_by_book_and_customer(book.id, customer.id)
            estoque = Estoque.objects.get(book=book)
            estoque.increment_quantity()
            estoque.set_status()
            
            if borrow:
                self._conclude_borrow(borrow.id)
                return return_response(request, status.HTTP_200_OK, {'message': 'Book returned successfully'})
            
            return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Borrow not found'})
