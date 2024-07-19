from rest_framework import serializers 

from book_services.models import Borrow

class BorrowSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Borrow
        fields=[
            'id',
            'id_book',
            'id_customer',
            'initial_date',
            'final_date'
        ]
        
        