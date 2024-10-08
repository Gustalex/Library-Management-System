from abc import ABC, abstractmethod
from book.models import Estoque
from fine.models import Fine
from book_services.helper import find_reservation_by_book_and_customer

class HandleTemplate(ABC):
    def handle(self, book, customer, handle_strategy, initial_date = None, final_date = None):
        self.check_availability(book, customer)
        self.validate_customer(customer)
        self.create_handle(book, customer, handle_strategy, initial_date, final_date)
    
    @abstractmethod
    def create_handle(self, book, customer, handle_strategy, initial_date = None, final_date = None):
        pass

    @abstractmethod
    def check_availability(self, book, customer = None):
        pass
    
    @abstractmethod
    def validate_customer(self, customer):
        pass
    

class BorrowTemplate(HandleTemplate):
    def create_handle(self, book, customer, handle_strategy, initial_date, final_date):
        return handle_strategy.create_borrow(book, customer, initial_date, final_date)
    
    def check_availability(self, book, customer):
        reservation = find_reservation_by_book_and_customer(book.id, customer.id)
        estoque = Estoque.objects.filter(book=book, quantity__gt=0, status__in=['Available', 'Last Unit']).first()
        if not estoque and not reservation:
            raise Exception('Book is not available')
    
    def validate_customer(self, customer):
        if Fine.objects.filter(customer=customer).exists():
            raise Exception('Customer has a fine')


class ReservationTemplate(HandleTemplate):
    def create_handle(self, book, customer, handle_strategy, initial_date = None, final_date = None):
        return handle_strategy.create_reservation(book, customer)
    
    def check_availability(self, book, customer = None):
        estoque = Estoque.objects.filter(book=book, quantity__gt=0, status__in=['Available', 'Last Unit']).first()
        if not estoque:
            raise Exception('Book is not available')
    
    def validate_customer(self, customer):
        if Fine.objects.filter(customer=customer).exists():
            raise Exception('Customer has a fine')
    