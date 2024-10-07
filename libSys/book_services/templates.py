from abc import ABC 
from book.models import Estoque
from fine.models import Fine
from book_services.helper import find_reservation_by_book_and_customer

class BorrowTemplate(ABC):
    def borrow(self, book, customer, initial_date, final_date, borrow_strategy):
        self.check_availability(book, customer)
        self.validate_customer(customer)
        self.create_borrow(book, customer, initial_date, final_date, borrow_strategy)
        

    def create_borrow(self, book, customer, initial_date, final_date, borrow_strategy):
        return borrow_strategy.create_borrow(book, customer, initial_date, final_date)

    def check_availability(self, book, customer):
        reservation = find_reservation_by_book_and_customer(book.id, customer.id)
        estoque = Estoque.objects.filter(book=book, quantity__gt=0, status__in=['Available', 'Last Unit']).first()
        if not estoque and not reservation:
            raise Exception('Book is not available')

    def validate_customer(self, customer):
        if Fine.objects.filter(customer=customer).exists():
            raise Exception('Customer has a fine')


class ReservationTemplate(ABC):
    def reserve(self, book, customer, reservation_strategy):
        self.validate_customer(customer)
        self.create_reservation(book, customer, reservation_strategy)

    def create_reservation(self, book, customer, reservation_strategy):
        return reservation_strategy.create_reservation(book, customer)

        
    def check_availability(self, book):
        estoque = Estoque.objects.filter(book=book, quantity__gt=0, status__in=['Available', 'Last Unit']).first()
        if not estoque:
            raise Exception('Book is not available')

    def validate_customer(self, customer):
        if Fine.objects.filter(customer=customer).exists():
            raise Exception('Customer has a fine')

    