from rest_framework.serializers import ModelSerializer

from fine.models import Fine


class FineSerializer(ModelSerializer):
    class Meta:
        model = Fine
        fields = '__all__'