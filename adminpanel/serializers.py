from rest_framework import serializers
from users.models import User
from products.models import Product
from orders.models import Order, OrderItem


# ------------------------
# Admin User Serializer
# ------------------------
class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_blocked', 'date_joined', 'last_login']
        read_only_fields = ['id', 'date_joined', 'last_login']


# ------------------------
# Admin Product Serializer
# ------------------------
class AdminProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'room', 'image', 'stock', 'is_archived', 'created_at']
        read_only_fields = ['id', 'created_at']


# ------------------------
# Admin Order Item Serializer
# ------------------------
class AdminOrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_title', 'quantity', 'subtotal']

    def get_subtotal(self, obj):
        return obj.subtotal()


# ------------------------
# Admin Order Serializer
# ------------------------
class AdminOrderSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    items = AdminOrderItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'total', 'address', 'payment_method', 'status', 'date']
        read_only_fields = ['id', 'user', 'items', 'total', 'date']
