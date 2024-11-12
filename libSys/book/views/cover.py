from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from book.models import Cover
from book.decorators import validade_book_exists, validate_cover_image

class CoverViewSet(ViewSet):
    parser_classes = (MultiPartParser, FormParser)

    @validade_book_exists
    @validate_cover_image
    @action(detail=True, methods=['post'])
    def cover(self, request, book, cover_image, pk=None):
        cover = Cover(book=book, cover_image=cover_image)
        cover.save()
        return Response({'message': 'Cover uploaded successfully'}, status=status.HTTP_200_OK)

    @validade_book_exists
    @validate_cover_image
    @action(detail=True, methods=['post'])
    def update_cover(self, request, book, cover_image, pk=None):
        cover = Cover.objects.filter(book=book).first()
        if cover:
            cover.hard_delete()
        new_cover = Cover(book=book, cover_image=cover_image)
        new_cover.save()
        return Response({'message': 'Cover updated successfully'}, status=status.HTTP_200_OK)