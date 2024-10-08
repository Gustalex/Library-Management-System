from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import status
from django.db import transaction
from book_services.helper import return_response
from book_services.models import Borrow
from user.models import Customer
from fine.models import Fine
from fine.serializers import FineSerializer

from django_filters.rest_framework import DjangoFilterBackend
from fine.filters import FineFilter

class FineViewSet(ViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = FineFilter
    
    @action(detail=True, methods=['POST'])
    def create_new_fine(self, request):
        customer_id = request.data.get('customer_id')
        borrow_id = request.data.get('borrow_id')
        
        try:
            customer = Customer.objects.get(id=customer_id)
            borrow = Borrow.objects.get(id=borrow_id)
            value = borrow.calculate_fine()
            
            if value == 0:
                return return_response(request, status.HTTP_200_OK, {'message': 'No fine to be paid'})
            
        except Customer.DoesNotExist:
            return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Customer not found'})
        except Borrow.DoesNotExist:
            return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Borrow not found'})
        
        with transaction.atomic():
            fine = Fine.objects.create(customer=customer, borrow=borrow, value=value)
            return return_response(request, status.HTTP_201_CREATED, FineSerializer(fine).data)


    
    @action(detail=True, methods=['DELETE'])
    def conclude_fine(self, request, pk=None):
        try:
            fine = Fine.objects.get(id=pk)
        except Fine.DoesNotExist:
            return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Fine not found'})
        
        fine.conclude_fine()
        fine.delete()
        return return_response(request, status.HTTP_200_OK, FineSerializer(fine).data)
    
    @action(detail=False, methods=['GET'])
    def list_fines(self, request):
        try:
            filter_backends=self.filter_backends
            queryset = Fine.objects.filter(status=True)
            filtered_queryset = DjangoFilterBackend().filter_queryset(request, queryset, self)
            serializer=FineSerializer(filtered_queryset, many=True)
            return return_response(request, status.HTTP_200_OK, serializer.data)
        except Fine.DoesNotExist:
            return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'No fines found'})
    
    
        
    
    
    