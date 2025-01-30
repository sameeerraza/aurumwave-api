from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from account.serializers import EndUserSerializer

from product.models import Product


class RequestListCreateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    created_at = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        price = validated_data.get('price')
        estimated_profit = price * 0.25
        validated_data['estimated_profit'] = estimated_profit
        return super().create(validated_data)
