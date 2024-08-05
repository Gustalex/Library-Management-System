from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import status
from django.db import transaction
from book_services.helper import return_response
from book_services.models import Borrow
from user.models import Customer
from fine.models import Fine
from fine.serializers import FineSerializer

class FineViewSet(ViewSet):
    
    @action(detail=True, methods=['POST'])
    def creat_new_fine(self, request):
        try:
            customer = Customer.objects.get(id=request.data['customer_id'])
            borrow = Borrow.objects.get(id=request.data['borrow_id'])
            value = borrow.calculate_fine()
            if value == 0:
                return return_response(request, status.HTTP_400_BAD_REQUEST, {'message': 'No fine to be paid'})
        except Customer.DoesNotExist:
            return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Customer not found'})
        except Borrow.DoesNotExist:
            return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Borrow not found'})
        
        with transaction.atomic():
            fine = Fine.objects.create(customer=customer, borrow=borrow, value=value)
            return return_response(request, status.HTTP_201_CREATED, FineSerializer(fine).data)
    
    @action(detail=True, methods=['PATCH'])
    def conclude_fine(self, request, pk=None):
        try:
            fine = Fine.objects.get(id=pk)
        except Fine.DoesNotExist:
            return return_response(request, status.HTTP_404_NOT_FOUND, {'message': 'Fine not found'})
        
        fine.conclude_fine()
        return return_response(request, status.HTTP_200_OK, FineSerializer(fine).data)
    
    @action(detail=False, methods=['GET'])
    def list_fines(self, request):
        fines = Fine.objects.filter(status=True)
        return return_response(request, status.HTTP_200_OK, FineSerializer(fines, many=True).data)
    
    
        
    
    
    