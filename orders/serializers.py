


from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='product.title', read_only=True)
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    image = serializers.CharField(source='product.image', read_only=True)
    quantity = serializers.IntegerField()

    class Meta:
        model = OrderItem
        fields = ['id', 'title', 'price', 'image', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'total', 'address', 'payment_method', 'status', 'date', 'items']
        read_only_fields = ['status', 'date', 'total']
