from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CartItem, Product
from .serializers import CartItemSerializer

class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # Get all cart items
    def get(self, request):
        items = CartItem.objects.filter(user=request.user)
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)

    # Add item to cart
    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        if not product_id:
            return Response({"error": "Product ID is required"}, status=400)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        # Check if item is already in cart
        if CartItem.objects.filter(user=request.user, product=product).exists():
            return Response({"error": "Item already in cart"}, status=400)

        # Create new cart item
        item = CartItem.objects.create(user=request.user, product=product, quantity=quantity)
        serializer = CartItemSerializer(item)
        return Response(serializer.data, status=201)

    # Update quantity of an item
    def put(self, request, pk):
        try:
            item = CartItem.objects.get(pk=pk, user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)

        quantity = request.data.get("quantity")
        if quantity is not None and int(quantity) > 0:
            item.quantity = int(quantity)
            item.save()
        else:
            return Response({"error": "Invalid quantity"}, status=400)

        serializer = CartItemSerializer(item)
        return Response(serializer.data)

    # Delete a single item
    def delete(self, request, pk):
        try:
            item = CartItem.objects.get(pk=pk, user=request.user)
            item.delete()
            return Response({"message": "Item removed"}, status=204)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)


# Clear all cart items
class ClearCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        CartItem.objects.filter(user=request.user).delete()
        return Response({"message": "Cart cleared"}, status=204)
