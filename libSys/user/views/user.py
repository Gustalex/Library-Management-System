from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

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

