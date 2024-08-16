from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from book.models.factory_model import FactoryModel
from book.models.book import Book

class Cover(FactoryModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='covers')
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    
    class Meta:
        db_table = 'cover'
        verbose_name = 'Cover'
        verbose_name_plural = 'Covers'
        ordering = ['id']
    
    def __str__(self) -> str:
        return self.book.title

@receiver(post_delete, sender=Cover)
def delete_cover_image(sender, instance, **kwargs):
    if instance.cover_image:
        instance.cover_image.delete(False)
