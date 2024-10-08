from django.urls import path, include
from rest_framework.routers import DefaultRouter
from book.views import BookViewSet, GenreViewSet, CoverViewSet, EstoqueViewSet

router = DefaultRouter()
router.register(r'book', BookViewSet, basename='book')
router.register(r'genre', GenreViewSet, basename='genre')
router.register(r'covers', CoverViewSet, basename='cover')
router.register(r'estoque', EstoqueViewSet, basename='estoque')

urlpatterns = [
    path('', include(router.urls)),
    path('check_isbn/', BookViewSet.as_view({'get': 'check_isbn'}), name='check_isbn'),
    path('cover/<int:pk>/', CoverViewSet.as_view({'post':'update_cover'}), name='update_cover'),
]
