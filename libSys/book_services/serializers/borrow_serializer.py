from rest_framework import serializers
from book_services.models import Borrow
from user.models import Customer
from book.models import Book

class BorrowSerializer(serializers.ModelSerializer):
    book_name = serializers.SerializerMethodField()
    customer_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Borrow
        fields = [
            'id',
            'book',
            'book_name',
            'customer',
            'customer_name',
            'initial_date',
            'final_date',
            'active',
        ]
    
    def get_book_name(self, obj):
        return obj.book.title 
    
    def get_customer_name(self, obj):
        return obj.customer.name
