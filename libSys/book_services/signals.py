from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from book_services.models import (Reservation, Borrow)


@receiver(post_save, sender=Borrow)
def add_borrowed_book(sender, instance, created, **kwargs):
    if created:
        customer = instance.customer
        customer.borrows.add(instance)

@receiver(post_delete, sender=Borrow)
def remove_borrowed_book(sender, instance, **kwargs):
    customer = instance.customer
    customer.borrows.remove(instance)

@receiver(post_save, sender=Reservation)
def add_reserved_book(sender, instance, created, **kwargs):
    if created:
        customer = instance.customer
        customer.reservations.add(instance)

@receiver(post_delete, sender=Reservation)
def remove_reserved_book(sender, instance, **kwargs):
    customer = instance.customer
    customer.reservations.remove(instance)
