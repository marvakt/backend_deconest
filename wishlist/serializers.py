from rest_framework import serializers
from .models import Wishlist
from products.models import Product
from products.serializers import ProductSerializer


class UserReferenceMixin(serializers.ModelSerializer):
    """Automatically assign logged-in user on create."""
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class WishlistSerializer(UserReferenceMixin, serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product', 'product_id']
        read_only_fields = ['user']

    def validate(self, data):
        """Prevent duplicate wishlist entries."""
        user = self.context['request'].user
        product = data['product']
        if Wishlist.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("This product is already in your wishlist.")
        return data




