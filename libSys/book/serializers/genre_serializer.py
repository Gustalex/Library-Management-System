from rest_framework import serializers

from libSys.book.models.genre import Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model=Genre
        fields='__all__'
