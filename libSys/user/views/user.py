from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from user.models import Customer
from user.serializers.user_serializer import CustomerSerializer, CustomerCreateSerializer, CustomerUpdateSerializer

class CustomerListCreateView(ListCreateAPIView):
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CustomerCreateSerializer
        return CustomerSerializer
    
class CustomerRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer
    
    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return CustomerUpdateSerializer
        return CustomerSerializer

class CustomerViewSet(ViewSet):
    
    @action(detail=False, methods=['get'])
    def check_cpf(self, request):
        cpf=request.query_params.get('cpf', None)
        
        if cpf is not None:
            customers=Customer.objects.filter(cpf=cpf)
            serializer=CustomerSerializer(customers, many=True)
            return Response(serializer.data)
        
        return Response({'detail': 'CPF não informado.'}, status=status.HTTP_400_BAD_REQUEST)