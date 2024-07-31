from datetime import datetime

from rest_framework.response import Response

from book.models import Book, Estoque
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
        
    return Reservation.objects.filter(book=book, customer=customer, active=True).first()


def check_stock(book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return False
        
        estoque = Estoque.objects.filter(book=book, quantity__gt=0, status__in=['Available', 'Last Unit'])
        return estoque.exists()
