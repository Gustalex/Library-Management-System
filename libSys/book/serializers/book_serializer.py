from rest_framework import serializers

from book.models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        extra_kwargs = {
            'isbn': {'validators': []},
        }


class UpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=[]

