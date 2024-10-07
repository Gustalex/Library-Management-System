from django.db import transaction

from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import status

from book_services.helper import return_response, check_stock
from book_services.models import Borrow, Reservation
from book_services.factories import get_borrow_creator 
from book_services.templates import BorrowTemplate

from user.models import Customer
from book.models import Book, Estoque
from fine.models import Fine

from book_services.serializers import BorrowSerializer

from django_filters.rest_framework import DjangoFilterBackend
from book_services.filters import BorrowFilter

class BorrowViewSet(ViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = BorrowFilter

    @action(detail=True, methods=['POST'])
    def do_borrow(self, request, pk=None):
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
            fine=Fine.objects.filter(customer=customer)
            if fine.exists():
                return return_response(request, status.HTTP_400_BAD_REQUEST, {'message': 'Customer has a fine to pay'})
            
            borrow_template = BorrowTemplate()
            
            if not check_stock(book.id) and not Reservation.objects.filter(book=book, customer=customer, active=True).exists():
                return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Book is not available'})
                            
            try:
                borrow_strategy = get_borrow_creator(book, customer)
                borrow = borrow_template.borrow(book, customer, initial_date, final_date, borrow_strategy)
                return return_response(request, status.HTTP_201_CREATED, {'message': 'Borrow created'})
            except Exception as e:
                return return_response(request, status.HTTP_400_BAD_REQUEST, {'message': str(e)})
            
        return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Book is not available'})
                
                
    @action(detail=True, methods=['DELETE'])
    def delete_borrow(self, request, pk=None):
        try:
            borrow = Borrow.objects.get(id=pk)
        except Borrow.DoesNotExist:
            return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Borrow not found'})
        with transaction.atomic():
            estoque=Estoque.objects.get(book=borrow.book)
            estoque.increment_quantity()
            estoque.set_status()
            borrow.cancel_borrow()
            borrow.delete()
        return return_response(request, status.HTTP_200_OK, {'message': 'Borrow deleted'})
    
    @action(detail=False, methods=['GET'])
    def list_borrows(self, request):
        try:
            filter_backends = self.filter_backends
            queryset = Borrow.objects.filter(active=True)
            filtered_queryset=DjangoFilterBackend().filter_queryset(request, queryset, self)
            serializer=BorrowSerializer(filtered_queryset, many=True)
            return return_response(request, status.HTTP_200_OK, serializer.data)
        except Borrow.DoesNotExist:
            return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Borrows not found'})
        
    
    @action(detail=True, methods=['GET'])
    def get_borrow(self, request, pk=None):
        try:
            borrow = Borrow.objects.get(id=pk)
            serializer = BorrowSerializer(borrow)
            return return_response(request, status.HTTP_200_OK, serializer.data)
        except Borrow.DoesNotExist:
            return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Borrow not found'})