from rest_framework import serializers

from book.models import Estoque, Book

class EstoqueSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Estoque
        fields = '__all__'
        extra_kwargs = {
            'quantity': {'required': False},
            'status': {'required': False},
        }