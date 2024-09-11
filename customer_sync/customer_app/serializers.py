from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id','name','email')

class hookserializer(serializers.Serializer):
    id = serializers.CharField(max_length=50)
    type = serializers.CharField(max_length=50)
    data = serializers.JSONField()
    created = serializers.IntegerField()