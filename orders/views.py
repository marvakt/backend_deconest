

# from rest_framework import permissions, status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.db import transaction

# from cart.models import CartItem
# from .models import Order, OrderItem
# from .serializers import OrderSerializer


# # ---------------------------
# # ✅ USER: View All Orders
# # ---------------------------
# class OrderView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         """Users see only their orders, Admins see all."""
#         user = request.user
#         orders = Order.objects.all() if user.is_staff else Order.objects.filter(user=user)
#         serializer = OrderSerializer(orders, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         """Place order directly (used by Checkout). Backend handles all logic."""
#         user = request.user
#         cart_items = CartItem.objects.filter(user=user)

#         if not cart_items.exists():
#             return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

#         address = request.data.get('address', '').strip()
#         if not address:
#             return Response({'error': 'Address is required'}, status=status.HTTP_400_BAD_REQUEST)

#         payment_method = request.data.get('payment_method', 'Cash on Delivery')
#         if payment_method.lower() in ['cod', 'cash on delivery', 'cash']:
#             payment_method = 'Cash on Delivery'

#         total = sum(item.product.price * item.quantity for item in cart_items)

#         # Atomic transaction ensures all or nothing
#         with transaction.atomic():
#             order = Order.objects.create(
#                 user=user,
#                 total=total,
#                 address=address,
#                 payment_method=payment_method
#             )

#             order_items = [
#                 OrderItem(order=order, product=item.product, quantity=item.quantity)
#                 for item in cart_items
#             ]
#             OrderItem.objects.bulk_create(order_items)

#             # Clear cart after placing order
#             cart_items.delete()

#         serializer = OrderSerializer(order)
#         return Response(
#             {'message': 'Order placed successfully', 'order': serializer.data},
#             status=status.HTTP_201_CREATED
#         )


# # ---------------------------
# # ✅ USER: Checkout Confirmation (clean + safe)
# # ---------------------------
# class CheckoutView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         print("========== DEBUG Checkout ==========")
#         print("User:", request.user)
#         print("Is Authenticated:", request.user.is_authenticated)
#         print("Request Data:", request.data)

#         user = request.user
#         cart_items = CartItem.objects.filter(user=user)

#         if not cart_items.exists():
#             print("DEBUG: Cart empty for user", user)
#             return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

#         address = request.data.get('address', '').strip()
#         if not address:
#             print("DEBUG: Missing address")
#             return Response({'error': 'Address is required'}, status=status.HTTP_400_BAD_REQUEST)

#         payment_method = request.data.get('payment_method', 'Cash on Delivery')
#         if payment_method.lower() in ['cod', 'cash on delivery', 'cash']:
#             payment_method = 'Cash on Delivery'

#         total = sum(item.product.price * item.quantity for item in cart_items)

#         with transaction.atomic():
#             order = Order.objects.create(
#                 user=user,
#                 total=total,
#                 address=address,
#                 payment_method=payment_method
#             )

#             order_items = [
#                 OrderItem(order=order, product=item.product, quantity=item.quantity)
#                 for item in cart_items
#             ]
#             OrderItem.objects.bulk_create(order_items)
#             cart_items.delete()

#         serializer = OrderSerializer(order)
#         return Response({'message': 'Order placed successfully', 'order': serializer.data}, status=status.HTTP_201_CREATED)

# # ---------------------------
# # ✅ USER: Latest Order Summary
# # ---------------------------
# class LatestOrderView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         """Fetch the most recent order for logged-in user."""
#         latest_order = Order.objects.filter(user=request.user).order_by('-date').first()
#         if not latest_order:
#             return Response({"error": "No orders found"}, status=status.HTTP_404_NOT_FOUND)
#         serializer = OrderSerializer(latest_order)
#         return Response(serializer.data, status=status.HTTP_200_OK)



from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction

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
        serializer = OrderSerializer(orders, many=True, context={'request': request})  # ✅ Added context
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Place order directly (used by Checkout). Backend handles all logic."""
        user = request.user
        cart_items = CartItem.objects.filter(user=user)

        if not cart_items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        address = request.data.get('address', '').strip()
        if not address:
            return Response({'error': 'Address is required'}, status=status.HTTP_400_BAD_REQUEST)

        payment_method = request.data.get('payment_method', 'Cash on Delivery')
        if payment_method.lower() in ['cod', 'cash on delivery', 'cash']:
            payment_method = 'Cash on Delivery'

        total = sum(item.product.price * item.quantity for item in cart_items)

        # Atomic transaction ensures all or nothing
        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                total=total,
                address=address,
                payment_method=payment_method
            )

            order_items = [
                OrderItem(order=order, product=item.product, quantity=item.quantity)
                for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)

            # Clear cart after placing order
            cart_items.delete()

        serializer = OrderSerializer(order, context={'request': request})  # ✅ Added context
        return Response(
            {'message': 'Order placed successfully', 'order': serializer.data},
            status=status.HTTP_201_CREATED
        )


# ---------------------------
# ✅ USER: Checkout Confirmation (clean + safe)
# ---------------------------
class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        print("========== DEBUG Checkout ==========")
        print("User:", request.user)
        print("Is Authenticated:", request.user.is_authenticated)
        print("Request Data:", request.data)

        user = request.user
        cart_items = CartItem.objects.filter(user=user)

        if not cart_items.exists():
            print("DEBUG: Cart empty for user", user)
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        address = request.data.get('address', '').strip()
        if not address:
            print("DEBUG: Missing address")
            return Response({'error': 'Address is required'}, status=status.HTTP_400_BAD_REQUEST)

        payment_method = request.data.get('payment_method', 'Cash on Delivery')
        if payment_method.lower() in ['cod', 'cash on delivery', 'cash']:
            payment_method = 'Cash on Delivery'

        total = sum(item.product.price * item.quantity for item in cart_items)

        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                total=total,
                address=address,
                payment_method=payment_method
            )

            order_items = [
                OrderItem(order=order, product=item.product, quantity=item.quantity)
                for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)
            cart_items.delete()

        serializer = OrderSerializer(order, context={'request': request})  # ✅ Added context
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
        serializer = OrderSerializer(latest_order, context={'request': request})  # ✅ Added context
        return Response(serializer.data, status=status.HTTP_200_OK)
