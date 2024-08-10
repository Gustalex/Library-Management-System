from rest_framework import serializers

from user.models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields=[
            'id',
            'name',
            'email',
            'cpf',
            'reservations',
            'borrows',
            'fines',
        ]

class CustomerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields=[
            'name',
            'email',
            'cpf',
        ]
    
    def create(self, validated_data):
        customer=Customer.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            cpf=validated_data['cpf'],
        )
        return customer

class CustomerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields=[
            'name',
            'email',
            'cpf',
        ]
    
    def update(self, instance, validated_data):
        instance.name=validated_data.get('name', instance.name)
        instance.email=validated_data.get('email', instance.email)
        instance.cpf=validated_data.get('cpf', instance.cpf)
        instance.save()
        return instance