from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from book.models import Book, Estoque
from book.serializers import BookSerializer

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        isbn = serializer.validated_data['isbn']
        
        if Book.objects.filter(isbn=isbn).exists():
            book = Book.objects.get(isbn=isbn)
            estoque = Estoque.objects.filter(book=book).first()
            if estoque:
                estoque.quantity += 1
                estoque.set_status()
                estoque.save()
                return Response({'detail': 'Quantidade incrementada no estoque.'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Estoque não encontrado para o livro existente.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            book = serializer.save()
            Estoque.objects.create(book=book, quantity=1)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
