
# from rest_framework import permissions, status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from django.db import transaction
# from django.conf import settings
# import razorpay
# import hmac, hashlib

# from cart.models import CartItem
# from .models import Order, OrderItem
# from .serializers import OrderSerializer

# # ---------------------------
# # ✅ User: View & Place Orders
# # ---------------------------
# class OrderView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         orders = Order.objects.all() if user.is_staff else Order.objects.filter(user=user)
#         serializer = OrderSerializer(orders, many=True, context={'request': request})
#         return Response(serializer.data)

#     def post(self, request):
#         """Place COD order"""
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

#         with transaction.atomic():
#             order = Order.objects.create(
#                 user=user,
#                 total=total,
#                 address=address,
#                 payment_method=payment_method,
#                 is_paid=(payment_method != "Cash on Delivery")
#             )
#             order_items = [OrderItem(order=order, product=item.product, quantity=item.quantity)
#                            for item in cart_items]
#             OrderItem.objects.bulk_create(order_items)
#             cart_items.delete()

#         serializer = OrderSerializer(order, context={'request': request})
#         return Response({'message': 'Order placed successfully', 'order': serializer.data},
#                         status=status.HTTP_201_CREATED)


# class CheckoutView(OrderView):
#     """Checkout uses the same logic as OrderView for COD"""
#     pass


# class LatestOrderView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         latest_order = Order.objects.filter(user=request.user).order_by('-date').first()
#         if not latest_order:
#             return Response({"error": "No orders found"}, status=status.HTTP_404_NOT_FOUND)
#         serializer = OrderSerializer(latest_order, context={'request': request})
#         return Response(serializer.data)


# # -------------------- Razorpay client --------------------
# client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


# @api_view(['POST'])
# def create_razorpay_order(request):
#     """Create Razorpay order"""
#     user = request.user
#     cart_items = CartItem.objects.filter(user=user)

#     if not cart_items.exists():
#         return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

#     total = sum(item.product.price * item.quantity for item in cart_items)
#     if total <= 0:
#         return Response({'error': 'Cart total is zero'}, status=status.HTTP_400_BAD_REQUEST)

#     amount_in_paise = int(total * 100)

#     try:
#         razorpay_order = client.order.create({
#             "amount": amount_in_paise,
#             "currency": "INR",
#             "payment_capture": 1
#         })
#         print("Razorpay order created:", razorpay_order)
#     except Exception as e:
#         print("Razorpay order creation error:", str(e))
#         return Response({'error': f'Razorpay order creation failed: {str(e)}'},
#                         status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     return Response({
#         "order_id": razorpay_order['id'],
#         "amount": amount_in_paise,
#         "currency": "INR",
#         "key": settings.RAZORPAY_KEY_ID
#     })


# @api_view(['POST'])
# def verify_razorpay_payment(request):
#     """Verify Razorpay payment and create order"""
#     user = request.user
#     data = request.data

#     print("Verify request data:", data)

#     required_fields = ['razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature']
#     if not all(field in data for field in required_fields):
#         return Response(
#             {'status': 'failure', 'error': 'Missing payment fields'},
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     try:
#         # Step 1: Signature verification
#         msg = f"{data['razorpay_order_id']}|{data['razorpay_payment_id']}"
#         generated_signature = hmac.new(
#             settings.RAZORPAY_KEY_SECRET.encode(),
#             msg.encode(),
#             hashlib.sha256
#         ).hexdigest()  # ⚡ Use hexdigest instead of base64

#         print("Generated signature:", generated_signature)
#         print("Received signature:", data['razorpay_signature'])

#         if not hmac.compare_digest(generated_signature, data['razorpay_signature']):
#             return Response(
#                 {'status': 'failure', 'error': 'Invalid signature'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Step 2: Payment verified, create order
#         cart_items = CartItem.objects.filter(user=user)
#         if not cart_items.exists():
#             return Response(
#                 {'status': 'failure', 'error': 'Cart is empty'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         address = data.get('address', '').strip()
#         if not address:
#             address = 'No address provided'

#         total = sum(item.product.price * item.quantity for item in cart_items)

#         with transaction.atomic():
#             order = Order.objects.create(
#                 user=user,
#                 total=total,
#                 address=address,
#                 payment_method='Razorpay Online Payment',
#                 payment_id=data['razorpay_payment_id'],
#                 is_paid=True
#             )

#             order_items = [OrderItem(order=order, product=item.product, quantity=item.quantity)
#                            for item in cart_items]
#             OrderItem.objects.bulk_create(order_items)
#             cart_items.delete()

#         serializer = OrderSerializer(order, context={'request': request})
#         return Response({'status': 'success', 'order': serializer.data})

#     except Exception as e:
#         print("Verification error:", str(e))
#         return Response(
#             {'status': 'failure', 'error': str(e)},
#             status=status.HTTP_400_BAD_REQUEST
#         )

from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import transaction
from django.conf import settings
import razorpay, hmac, hashlib

from cart.models import CartItem
from .models import Order, OrderItem
from .serializers import OrderSerializer

# --------------------------- Orders Views ---------------------------

class OrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """✅ Show only logged-in user's orders (no exceptions)"""
        orders = (
            Order.objects.filter(user=request.user)
            .prefetch_related("items", "items__product")
            .order_by("-date")
        )
        serializer = OrderSerializer(orders, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        """Place COD order"""
        user = request.user
        cart_items = CartItem.objects.filter(user=user)
        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        address = request.data.get("address", "").strip()
        if not address:
            return Response({"error": "Address is required"}, status=status.HTTP_400_BAD_REQUEST)

        payment_method = request.data.get("payment_method", "Cash on Delivery")
        if payment_method.lower() in ["cod", "cash on delivery", "cash"]:
            payment_method = "Cash on Delivery"

        total = sum(item.product.price * item.quantity for item in cart_items)

        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                total=total,
                address=address,
                payment_method=payment_method,
                is_paid=(payment_method != "Cash on Delivery"),
            )
            order_items = [
                OrderItem(order=order, product=item.product, quantity=item.quantity)
                for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)
            cart_items.delete()

        serializer = OrderSerializer(order, context={"request": request})
        return Response(
            {"message": "Order placed successfully", "order": serializer.data},
            status=status.HTTP_201_CREATED,
        )


class LatestOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """✅ Only user's latest order"""
        latest_order = (
            Order.objects.filter(user=request.user).order_by("-date").first()
        )
        if not latest_order:
            return Response({"error": "No orders found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(latest_order, context={"request": request})
        return Response(serializer.data)


# -------------------- Razorpay Integration --------------------
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@api_view(["POST"])
def create_razorpay_order(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    if not cart_items.exists():
        return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

    total = sum(item.product.price * item.quantity for item in cart_items)
    amount_in_paise = int(total * 100)

    try:
        razorpay_order = client.order.create({
            "amount": amount_in_paise,
            "currency": "INR",
            "payment_capture": 1,
        })
    except Exception as e:
        return Response(
            {"error": f"Razorpay order creation failed: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return Response({
        "order_id": razorpay_order["id"],
        "amount": amount_in_paise,
        "currency": "INR",
        "key": settings.RAZORPAY_KEY_ID,
    })


@api_view(["POST"])
def verify_razorpay_payment(request):
    user = request.user
    data = request.data

    required_fields = ["razorpay_order_id", "razorpay_payment_id", "razorpay_signature"]
    if not all(field in data for field in required_fields):
        return Response(
            {"status": "failure", "error": "Missing payment fields"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        msg = f"{data['razorpay_order_id']}|{data['razorpay_payment_id']}"
        generated_signature = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode(),
            msg.encode(),
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(generated_signature, data["razorpay_signature"]):
            return Response(
                {"status": "failure", "error": "Invalid signature"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Payment verified, create order
        cart_items = CartItem.objects.filter(user=user)
        if not cart_items.exists():
            return Response(
                {"status": "failure", "error": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        address = data.get("address", "").strip() or "No address provided"
        total = sum(item.product.price * item.quantity for item in cart_items)

        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                total=total,
                address=address,
                payment_method="Razorpay Online Payment",
                payment_id=data["razorpay_payment_id"],
                is_paid=True,
            )
            order_items = [
                OrderItem(order=order, product=item.product, quantity=item.quantity)
                for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)
            cart_items.delete()

        serializer = OrderSerializer(order, context={"request": request})
        return Response({"status": "success", "order": serializer.data})

    except Exception as e:
        return Response(
            {"status": "failure", "error": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )
