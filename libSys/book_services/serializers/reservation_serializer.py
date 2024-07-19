from rest_framework import serializers

from book_services.models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Reservation
        fields=[
            'id',
            'id_book',
            'id_customer'
        ]