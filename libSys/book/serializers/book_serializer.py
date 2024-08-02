from rest_framework import serializers
from book.models import Book, Genre
from book.models.cover import Cover

class CoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cover
        fields = ['cover_image']

class BookSerializer(serializers.ModelSerializer):
    covers = CoverSerializer(many=True, read_only=True)
    genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all())

    class Meta:
        model = Book
        fields = '__all__'
        extra_kwargs = {
            'isbn': {'validators': []},
        }

class UpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = []
