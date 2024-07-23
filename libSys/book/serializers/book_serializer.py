from rest_framework import serializers

from book.models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=[
            'id',
            'title',
            'author',
            'genre',
            'status',
            'synopsis'
        ]

class UpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=[]

