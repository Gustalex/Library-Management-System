from django.urls import path

from book_services.views import ReservationViewSet
from book_services.views import BorrowViewSet
from book_services.views import DevolutionViewSet
from book_services.views import PopularityViewSet
 
urlpatterns = [
    path('reserve/', ReservationViewSet.as_view({'post': 'do_reservation'}), name='do_reservation'),
    path('reserve/<int:pk>/delete/', ReservationViewSet.as_view({'delete': 'delete_reservation'}), name='delete_reservation'),
    path('borrow/', BorrowViewSet.as_view({'post': 'do_borrow'}), name='do_borrow'),
    path('borrow/<int:pk>/delete/', BorrowViewSet.as_view({'delete': 'delete_borrow'}), name='delete_borrow'),
    path('devolution/', DevolutionViewSet.as_view({'patch': 'do_devolution'}), name='do_devolution'),
    path('popular/', PopularityViewSet.as_view({'get': 'get_popular_books'}), name='get_popular_books'),
    path('borrow/loans/', BorrowViewSet.as_view({'get': 'list_borrows'}), name='list_borrows'),
    path('borrow/<int:pk>/get_loan/', BorrowViewSet.as_view({'get': 'get_borrow'}), name='get_borrow'),
]