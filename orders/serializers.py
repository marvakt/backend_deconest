# from rest_framework import serializers
# from .models import Order, OrderItem
# from products.serializers import ProductSerializer


# class UserReferenceMixin(serializers.ModelSerializer):
#     """Automatically assign logged-in user on create."""
#     def create(self, validated_data):
#         user = self.context['request'].user
#         validated_data['user'] = user
#         return super().create(validated_data)


# class OrderItemSerializer(serializers.ModelSerializer):
#     title = serializers.CharField(source='product.title', read_only=True)
#     price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
#     image = serializers.ImageField(source='product.image', read_only=True)

#     class Meta:
#         model = OrderItem
#         fields = ['id', 'title', 'price', 'image', 'quantity']



# class OrderSerializer(UserReferenceMixin, serializers.ModelSerializer):
#     items = OrderItemSerializer(many=True, read_only=True)
#     total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

#     class Meta:
#         model = Order
#         fields = ['id', 'user', 'total', 'address', 'payment_method', 'status', 'date', 'items']
#         read_only_fields = ['user', 'status', 'date', 'total']




from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer


class UserReferenceMixin(serializers.ModelSerializer):
    """Automatically assign logged-in user on create."""
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


# serializers.py

class OrderItemSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='product.title', read_only=True)
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    image = serializers.CharField(source='product.image', read_only=True)  # <-- this is important
    quantity = serializers.IntegerField()

    class Meta:
        model = OrderItem
        fields = ['id', 'title', 'price', 'image', 'quantity']

class OrderSerializer(UserReferenceMixin, serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'total', 'address', 'payment_method', 'status', 'date', 'items']
        read_only_fields = ['user', 'status', 'date', 'total']
