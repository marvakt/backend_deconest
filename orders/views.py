from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from cart.models import CartItem
from .models import Order, OrderItem
from .serializers import OrderSerializer


# ---------------------------
# ✅ USER: View All Orders
# ---------------------------
class OrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Users see only their orders, Admins see all."""
        user = request.user
        orders = Order.objects.all() if user.is_staff else Order.objects.filter(user=user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Place order directly (used by Checkout)."""
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        address = request.data.get('address')
        if not address:
            return Response({'error': 'Address is required'}, status=status.HTTP_400_BAD_REQUEST)

        payment_method = request.data.get('payment_method', 'COD')

        total = sum(item.product.price * item.quantity for item in cart_items)
        order = Order.objects.create(
            user=request.user,
            total=total,
            address=address,
            payment_method=payment_method
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )

        # Clear cart after order
        cart_items.delete()

        serializer = OrderSerializer(order)
        return Response(
            {'message': 'Order placed successfully', 'order': serializer.data},
            status=status.HTTP_201_CREATED
        )


# ---------------------------
# ✅ USER: Checkout Confirmation
# ---------------------------
class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Handles checkout flow (can be merged with OrderView.post if needed)."""
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        address = request.data.get('address')
        if not address:
            return Response({'error': 'Address is required'}, status=status.HTTP_400_BAD_REQUEST)

        total = sum(item.product.price * item.quantity for item in cart_items)
        payment_method = request.data.get('payment_method', 'COD')

        order = Order.objects.create(
            user=request.user,
            total=total,
            address=address,
            payment_method=payment_method
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )

        cart_items.delete()
        serializer = OrderSerializer(order)
        return Response(
            {'message': 'Order placed successfully', 'order': serializer.data},
            status=status.HTTP_201_CREATED
        )


# ---------------------------
# ✅ USER: Latest Order Summary
# ---------------------------
class LatestOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Fetch the most recent order for logged-in user."""
        latest_order = Order.objects.filter(user=request.user).order_by('-date').first()
        if not latest_order:
            return Response({"error": "No orders found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(latest_order)
        return Response(serializer.data, status=status.HTTP_200_OK)
