from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from book.models import Book, Cover

class CoverViewSet(ViewSet):
    parser_classes = (MultiPartParser, FormParser)

    @action(detail=True, methods=['post'])
    def cover(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

        cover_image = request.FILES.get('cover_image')
        if not cover_image:
            return Response({'error': 'No cover image provided'}, status=status.HTTP_400_BAD_REQUEST)

        cover = Cover(book=book, cover_image=cover_image)
        cover.save()

        return Response({'message': 'Cover uploaded successfully'}, status=status.HTTP_200_OK)
