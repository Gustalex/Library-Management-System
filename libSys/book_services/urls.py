from django.urls import path

from book_services.views import ReservationViewSet

urlpatterns = [
    path('reserve/', ReservationViewSet.as_view({'post': 'do_reservation'}), name='do_reservation'),
]