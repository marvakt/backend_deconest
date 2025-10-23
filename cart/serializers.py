from rest_framework import serializers
from .models import CartItem
from products.models import Product
from products.serializers import ProductSerializer


class UserReferenceMixin(serializers.ModelSerializer):
    """Automatically assign logged-in user on create."""
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class CartItemSerializer(UserReferenceMixin, serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'user', 'product', 'product_id', 'quantity']
        read_only_fields = ['user']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value
