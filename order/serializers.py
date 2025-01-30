from product.models import Product
from order.models import Order

from rest_framework import serializers

from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    product_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )  # Accept multiple product IDs in the request

    class Meta:
        model = Order
        fields = ["id", "status", "product_ids", "created_at", "updated_at"]
        read_only_fields = ["id", "status", "created_at", "updated_at"]

    def create(self, validated_data):
        product_ids = validated_data.pop("product_ids")  # Extract product IDs
        user = self.context["request"].user  # Get logged-in user
        order = Order.objects.create(user=user, status=0, **validated_data)
        products = Product.objects.filter(id__in=product_ids)  # Fetch products
        order.products.set(products)  # Assign products to order
        return order


#
# class OrderSerializer(serializers.ModelSerializer):
#     # status = serializers.CharField(source='__str__')
#     # rider = serializers.CharField(source='rider.username', read_only=True)
#     # requestee = serializers.CharField(source='requestee.username', read_only=True)
#     created_at = serializers.DateTimeField(
#         format='%Y-%m-%d %H:%M:%S', read_only=True)
#
#     class Meta:
#         model = Order
#         fields = '__all__'


# Serializer for lisitng all the available orders for a specifc user
class OrderListSerializer(serializers.ModelSerializer):
    # status = serializers.CharField(source='__str__')
    status = serializers.IntegerField()

    user = serializers.CharField(
        source='user.username', read_only=True)
    created_at = serializers.DateTimeField(
        format='%Y-%m-%d', read_only=True)
    title = serializers.CharField(source='request.title', read_only=True)
    image = serializers.CharField(source='request.image', read_only=True)

    class Meta:
        model = Order
        exclude = ('updated_at',)


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']


class OrderRequestSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Product
        fields = ('title', 'description', 'address', 'city', 'phone_number',
                  'country', 'price', 'estimated_profit', 'user', 'image')


class OrderDetailSerializer(serializers.ModelSerializer):
    status = serializers.IntegerField()
    created_at = serializers.DateTimeField(
        format='%Y-%m-%d', read_only=True)
    request = OrderRequestSerializer()

    class Meta:
        model = Order
        fields = ('status', 'score', 'created_at', 'request')
