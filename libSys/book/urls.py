from django.urls import path, include
from rest_framework.routers import DefaultRouter
from book.views import (BookViewSet, GenreViewSet)

router = DefaultRouter()
router.register(r'book', BookViewSet, basename='book')
router.register(r'genre', GenreViewSet, basename='genre')

urlpatterns = [
    path('', include(router.urls)),
]
