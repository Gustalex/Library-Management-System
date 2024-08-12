from django.urls import path

from .views import CustomerListCreateView, CustomerRetrieveUpdateDestroyView, CustomerViewSet

urlpatterns=[
    path('customers/', CustomerListCreateView.as_view(), name='customer-list-create'),
    path('customers/<int:pk>/', CustomerRetrieveUpdateDestroyView.as_view(), name='customer-retrieve-update-destroy'),
    path('customers/check-cpf/', CustomerViewSet.as_view({'get': 'check_cpf'}), name='customer-check-cpf'),
]