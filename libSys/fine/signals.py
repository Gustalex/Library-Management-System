from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Fine

@receiver(post_save, sender=Fine)
def add_fine(sender, instance, created, **kwargs):
    if created:
        customer = instance.customer
        customer.fines.add(instance)
    elif not instance.status:
        customer = instance.customer
        customer.fines.remove(instance)

@receiver(post_delete, sender=Fine)
def remove_fine(sender, instance, **kwargs):
    customer = instance.customer
    customer.fines.remove(instance)
