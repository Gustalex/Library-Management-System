from abc import ABC, abstractmethod
from book_services.helper import find_reservation_by_book_and_customer
from .strategies import StandardBorrowStrategy, ReservationBorrowStrategy, StandardReservationStrategy

class BorrowCreator(ABC):
    @abstractmethod
    def create_borrow(self, book, customer, initial_date, final_date):
        pass

class StandardBorrowCreator(BorrowCreator):
    def create_borrow(self, book, customer, initial_date, final_date):
        return StandardBorrowStrategy().create_borrow(book, customer, initial_date, final_date)

class ReservationBorrowCreator(BorrowCreator):
    def create_borrow(self, book, customer, initial_date, final_date):
        return ReservationBorrowStrategy().create_borrow(book, customer, initial_date, final_date)

class ReservationCreator(ABC):
    @abstractmethod
    def create_reservation(self, book, customer):
        pass

class StandardReservationCreator(ReservationCreator):
    def create_reservation(self, book, customer):
        return StandardReservationStrategy().create_reservation(book, customer)

def get_borrow_creator(book, customer):
    reservation = find_reservation_by_book_and_customer(book.id, customer.id)
    if reservation:
        return ReservationBorrowCreator()
    return StandardBorrowCreator()

def get_reservation_creator():
    return StandardReservationCreator()
