from rest_framework import serializers

from book_services.models import Popularity

class PopularitySerializer(serializers.ModelSerializer):
    
    class Meta: 
        model=Popularity
        fields=[
            'id',
            'id_book',
            'borrow_count'
        ]
    