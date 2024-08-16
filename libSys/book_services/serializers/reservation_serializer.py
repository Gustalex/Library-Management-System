from rest_framework import serializers

from book_services.models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    book_name=serializers.SerializerMethodField()
    customer_name=serializers.SerializerMethodField()
    customer_cpf=serializers.SerializerMethodField()
    class Meta:
        model=Reservation
        fields=[
            'id',
            'book',
            'book_name',
            'customer',
            'customer_name',
            'customer_cpf',
            'active',
        ]
        
    def get_book_name(self, obj):
        return obj.book.title 
    
    def get_customer_name(self, obj):
        return obj.customer.name
    
    def get_customer_cpf(self, obj):
        return obj.customer.cpf