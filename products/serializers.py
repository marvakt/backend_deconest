from rest_framework import serializers
from .models import Product


class TimestampSerializerMixin(serializers.ModelSerializer):
    """For models with created/updated timestamps."""
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        abstract = True


class ProductSerializer(TimestampSerializerMixin):
    class Meta:
        model = Product
        fields = '__all__'
