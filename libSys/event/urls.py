from django.urls import path, include
from rest_framework.routers import DefaultRouter
from event.views import EventViewSet

router = DefaultRouter()
router.register(r'event', EventViewSet, basename='event')

urlpatterns = [
    path('',include(router.urls)),
]
