from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import status
from django.db import transaction

from book_services.helper import return_response
from book_services.models import Reservation
from book_services.serializers import ReservationSerializer
from book_services.factories import get_reservation_creator
from book_services.templates import ReservationTemplate


from user.models import Customer
from book.models import Book, Estoque

from django_filters.rest_framework import DjangoFilterBackend
from book_services.filters import ReservationFilter

class ReservationViewSet(ViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReservationFilter
    
    @action(detail=False, methods=['POST'])
    def do_reservation(self, request):
        try:
            book = Book.objects.get(id=request.data['book_id'])
            customer = Customer.objects.get(id=request.data['customer_id'])
        except Book.DoesNotExist:
            return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Book not found'})
        except Customer.DoesNotExist:
            return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Customer not found'})
       
        reservation_template = ReservationTemplate()
        
        with transaction.atomic():
            try:
                reservation_strategy = get_reservation_creator()
                reservation = reservation_template.handle(book, customer, reservation_strategy)
                return return_response(request, status.HTTP_201_CREATED, {'message': 'Reservation created'})
            except Exception as e:
                return return_response(request, status.HTTP_400_BAD_REQUEST, {'message': str(e)})

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
    
    @action(detail=True, methods=['GET'])
    def get_reservation(self, request, pk=None):
        try:
            reservation=Reservation.objects.get(id=pk)
            serializer=ReservationSerializer(reservation)
            return return_response(request, status.HTTP_200_OK, serializer.data)
        except Reservation.DoesNotExist:
            return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Borrow not found'})
        
    @action(detail=False, methods=['GET'])
    def list_reservations(self, request):
        try:
            filter_backends=self.filter_backends
            queryset=Reservation.objects.filter(active=True)
            filtered_queryset=DjangoFilterBackend().filter_queryset(request, queryset, self)
            serializer=ReservationSerializer(filtered_queryset, many=True)
            return return_response(request, status.HTTP_200_OK, serializer.data)
        except Reservation.DoesNotExist:
            return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'No reservations found'})
        