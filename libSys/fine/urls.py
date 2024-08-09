from django.urls import path

from fine.views import FineViewSet

urlpatterns=[
    path('fine/', FineViewSet.as_view({'post': 'create_new_fine'}), name='create_new_fine'),
    path('fine/<int:pk>/conclude/', FineViewSet.as_view({'patch': 'conclude_fine'}), name='conclude_fine'),
    path('fine/list/', FineViewSet.as_view({'get': 'list_fines'}), name='list_fines'),
]