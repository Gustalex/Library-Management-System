from rest_framework import serializers

from book.models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=[
            'id',
            'title',
            'author',
            'id_genre',
            'book_status'
        ]

class UpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=[]

