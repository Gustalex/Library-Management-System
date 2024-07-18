from django.urls import path, include, re_path

from rest_framework.routers import DefaultRouter

from book.views import BookViewSet, GenreViewSet

router = DefaultRouter()

router.register(r'book', BookViewSet, basename='book')
router.register(r'genre', GenreViewSet, basename='genre')

urlpatterns = [     
    re_path(r'^', include(router.urls)),
    path('book/<int:pk>/reserve/', BookViewSet.as_view({'put': 'reserve_book'}), name='reserve_book'),
    path('book/<int:pk>/borrow/', BookViewSet.as_view({'put': 'borrow_book'}), name='borrow_book'),
    path('book/<int:pk>/return/', BookViewSet.as_view({'put': 'return_book'}), name='return_book'),
    path('book/<int:pk>/borrow_reserved/', BookViewSet.as_view({'put': 'borrow_reserved_book'}), name='borrow_reserved_book'),
]



