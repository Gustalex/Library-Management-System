from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from book_services.models import Popularity
from book.models.book import Book
from book.serializers import BookSerializer

class PopularityViewSet(ViewSet):

    @action(detail=False, methods=['get'])
    def get_popular_books(self, request):
        popular_books = Popularity.objects.order_by('-borrow_count')[:10]
        books = [pop.book for pop in popular_books]
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
