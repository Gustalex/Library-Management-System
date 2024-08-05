from django.db import models

from datetime import datetime 
from typing import Any

class FactoryManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_deleted=False)


class FactoryModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at=models.DateTimeField(auto_now=True, blank=True, null=True)
    is_deleted=models.BooleanField(default=False)
    deleted_at=models.DateTimeField(blank=True, null=True)
    objects=FactoryManager()
    all_objects=models.Manager()
    
    def hard_delete(self, using: Any=None, keep_parents: bool=False) -> tuple[int, dict[str, int]]:
        return super().delete(using, keep_parents)
    
    def delete(self):
        self.is_deleted=True
        self.deleted_at=datetime.now()
        self.save()
    
    def rollback(self):
        self.is_deleted=False
        self.deleted_at=None
        self.save()
    
    class Meta:
        abstract=True