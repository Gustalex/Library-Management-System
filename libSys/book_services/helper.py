from datetime import datetime

from rest_framework.response import Response

from book.models import Book
from user.models import Customer
from book_services.models import Reservation


def return_response(request, status, data):
    print(
        '[' + datetime.now().strftime('%d/%m/%Y %H:%M:%S') + ']',
        request.method,
        request.get_full_path(),
        status,
    )
    return Response(data, status=status)


def find_reservation_by_book_and_customer(book_id, customer_id):
    try:
        book = Book.objects.get(id=book_id)
        customer = Customer.objects.get(id=customer_id)
    except (Book.DoesNotExist, Customer.DoesNotExist):
        return None
        
    return Reservation.objects.filter(book=book, customer=customer, is_deleted=False).first()
