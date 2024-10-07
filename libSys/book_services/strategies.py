from abc import ABC, abstractmethod
from book_services.models import Borrow, Reservation, Popularity
from book.models import Estoque
from django.db import transaction

class BorrowStrategy(ABC):
    @abstractmethod
    def create_borrow(self, book, customer, initial_date, final_date):
        pass

class StandardBorrowStrategy(BorrowStrategy):
    def create_borrow(self, book, customer, initial_date, final_date):
        estoque = Estoque.objects.filter(book=book, quantity__gt=0, status__in=['Available', 'Last Unit']).first()
        if not estoque:
            raise Exception('Book is not available')

        with transaction.atomic():
            borrow = Borrow.objects.create(book=book, customer=customer, initial_date=initial_date, final_date=final_date)
            
            popularity, created = Popularity.objects.get_or_create(book=book)
            popularity.increment_borrow_count()
            
            estoque.decrement_quantity()
            estoque.set_status()
            estoque.save()
            
            return borrow

class ReservationBorrowStrategy(BorrowStrategy):
    def create_borrow(self, book, customer, initial_date, final_date):
        with transaction.atomic():
            reservation = Reservation.objects.get(book=book, customer=customer, active=True)
            reservation.inactivate_reservation()
            
            borrow = Borrow.objects.create(book=book, customer=customer, initial_date=initial_date, final_date=final_date)
            
            popularity, created = Popularity.objects.get_or_create(book=book)
            popularity.increment_borrow_count()
        
        return borrow

class ReservationStrategy(ABC):
    @abstractmethod
    def create_reservation(self, book, customer):
        pass

class StandardReservationStrategy(ReservationStrategy):
    def create_reservation(self, book, customer):
        estoque = Estoque.objects.filter(book=book, quantity__gt=0, status__in=['Available', 'Last Unit']).first()
        if not estoque:
            raise Exception('Book is not available')
        
        with transaction.atomic():
            reservation = Reservation.objects.create(book=book, customer=customer)
            estoque.decrement_quantity()
            estoque.set_status()
            
            return reservation
