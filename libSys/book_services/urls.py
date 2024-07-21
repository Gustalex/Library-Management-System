from django.urls import path

 

from book_services.views import ReservationViewSet
from book_services.views import BorrowViewSet
 
urlpatterns = [
    path('reserve/', ReservationViewSet.as_view({'post': 'do_reservation'}), name='do_reservation'),
    path('reserve/<int:pk>/cancel/', ReservationViewSet.as_view({'delete': 'cancel_reservation'}), name='cancel_reservation'),
    path('borrow/', BorrowViewSet.as_view({'post': 'do_borrow'}), name='do_borrow'),
    path('borrow/<int:pk>/', BorrowViewSet.as_view({'delete': 'delete_borrow'}), name='delete_borrow'),
]