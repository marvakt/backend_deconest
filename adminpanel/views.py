# # admin_views.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status, permissions
# from django.shortcuts import get_object_or_404
# from django.db.models import Sum

# from users.models import User
# from products.models import Product
# from orders.models import Order, OrderItem
# from .serializers import AdminUserSerializer, AdminProductSerializer, AdminOrderSerializer


# # ------------------------
# # Admin User Management
# # ------------------------
# class AdminUserListView(APIView):
#     permission_classes = [permissions.IsAdminUser]

#     def get(self, request):
#         users = User.objects.all()
#         serializer = AdminUserSerializer(users, many=True)
#         return Response(serializer.data)


# class AdminUserBlockView(APIView):
#     permission_classes = [permissions.IsAdminUser]

#     def post(self, request, pk):
#         user = get_object_or_404(User, pk=pk)
#         if user.role == 'admin':
#             return Response({'error': 'Cannot block another admin'}, status=status.HTTP_400_BAD_REQUEST)
#         user.is_blocked = True
#         user.save()
#         return Response({'message': f'User {user.username} blocked successfully'})


# class AdminUserUnblockView(APIView):
#     permission_classes = [permissions.IsAdminUser]

#     def post(self, request, pk):
#         user = get_object_or_404(User, pk=pk)
#         user.is_blocked = False
#         user.save()
#         return Response({'message': f'User {user.username} unblocked successfully'})


# # ------------------------
# # Admin Product Management
# # ------------------------
# class AdminProductListCreateView(APIView):
#     permission_classes = [permissions.IsAdminUser]

#     def get(self, request):
#         products = Product.objects.all()
#         serializer = AdminProductSerializer(products, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = AdminProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         data = serializer.validated_data
#         product = Product.objects.create(
#             title=data.get('title'),
#             description=data.get('description'),
#             price=data.get('price'),
#             room=data.get('room'),
#             image=data.get('image', None),
#             stock=data.get('stock', 0),
#             is_archived=data.get('is_archived', False)
#         )
#         return Response({'message': f'Product {product.title} created successfully'}, status=status.HTTP_201_CREATED)


# class AdminProductDetailView(APIView):
#     permission_classes = [permissions.IsAdminUser]

#     def get(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         serializer = AdminProductSerializer(product)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         serializer = AdminProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         data = serializer.validated_data

#         product.title = data.get('title', product.title)
#         product.description = data.get('description', product.description)
#         product.price = data.get('price', product.price)
#         product.room = data.get('room', product.room)
#         product.image = data.get('image', product.image)
#         product.stock = data.get('stock', product.stock)
#         product.is_archived = data.get('is_archived', product.is_archived)
#         product.save()

#         return Response({'message': f'Product {product.title} updated successfully'})


# class AdminProductArchiveView(APIView):
#     permission_classes = [permissions.IsAdminUser]

#     def post(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         product.is_archived = True
#         product.save()
#         return Response({'message': f'Product {product.title} archived successfully'})


# class AdminProductUnarchiveView(APIView):
#     permission_classes = [permissions.IsAdminUser]

#     def post(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         product.is_archived = False
#         product.save()
#         return Response({'message': f'Product {product.title} unarchived successfully'})


# # ------------------------
# # Admin Order Management
# # ------------------------
# class AdminOrderListView(APIView):
#     permission_classes = [permissions.IsAdminUser]

#     def get(self, request):
#         orders = Order.objects.all().order_by('-date')
#         serializer = AdminOrderSerializer(orders, many=True)
#         return Response(serializer.data)


# class AdminOrderTotalRevenueView(APIView):
#     permission_classes = [permissions.IsAdminUser]

#     def get(self, request):
#         total = Order.objects.aggregate(total_revenue=Sum('total'))['total_revenue'] or 0
#         return Response({'total_revenue': total})


# class AdminOrderTotalProductsSoldView(APIView):
#     permission_classes = [permissions.IsAdminUser]

#     def get(self, request):
#         result = OrderItem.objects.values('product__id', 'product__title') \
#             .annotate(total_sold=Sum('quantity')) \
#             .order_by('-total_sold')
#         return Response(result)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.db.models import Sum

from users.models import User
from products.models import Product
from orders.models import Order, OrderItem
from .serializers import AdminUserSerializer, AdminProductSerializer, AdminOrderSerializer


# ------------------------
# Admin User Management
# ------------------------
class AdminUserListView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = AdminUserSerializer(users, many=True)
        return Response(serializer.data)


class AdminUserBlockView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user.role == 'admin':
            return Response({'error': 'Cannot block another admin'}, status=status.HTTP_400_BAD_REQUEST)
        user.is_blocked = True
        user.save()
        return Response({'message': f'User {user.username} blocked successfully'})


class AdminUserUnblockView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.is_blocked = False
        user.save()
        return Response({'message': f'User {user.username} unblocked successfully'})


# ------------------------
# Admin Product Management
# ------------------------
class AdminProductListCreateView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        products = Product.objects.all()
        serializer = AdminProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AdminProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        product = Product.objects.create(
            title=data.get('title'),
            description=data.get('description'),
            price=data.get('price'),
            room=data.get('room'),
            image=data.get('image', None),
            stock=data.get('stock', 0),
            is_archived=data.get('is_archived', False)
        )
        return Response({'message': f'Product {product.title} created successfully'}, status=status.HTTP_201_CREATED)


class AdminProductDetailView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = AdminProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = AdminProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        product.title = data.get('title', product.title)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        product.room = data.get('room', product.room)
        product.image = data.get('image', product.image)
        product.stock = data.get('stock', product.stock)
        product.is_archived = data.get('is_archived', product.is_archived)
        product.save()

        return Response({'message': f'Product {product.title} updated successfully'})


class AdminProductArchiveView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_archived = True
        product.save()
        return Response({'message': f'Product {product.title} archived successfully'})


class AdminProductUnarchiveView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_archived = False
        product.save()
        return Response({'message': f'Product {product.title} unarchived successfully'})


# ------------------------
# Admin Order Management
# ------------------------
class AdminOrderListView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        """
        Get all orders, ordered by newest first
        """
        orders = Order.objects.all().order_by('-date')
        serializer = AdminOrderSerializer(orders, many=True)
        return Response(serializer.data)


class AdminOrderDetailView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, pk):
        """
        Get a single order by ID
        """
        order = get_object_or_404(Order, pk=pk)
        serializer = AdminOrderSerializer(order)
        return Response(serializer.data)

    def patch(self, request, pk):
        """
        Update order status
        """
        order = get_object_or_404(Order, pk=pk)
        status_value = request.data.get('status')
        if status_value not in ['Pending', 'Shipped', 'Delivered', 'Cancelled']:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        order.status = status_value
        order.save()
        return Response({'message': f'Order {order.id} status updated to {status_value}'})

    def delete(self, request, pk):
        """
        Delete an order
        """
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response({'message': f'Order {order.id} deleted successfully'}, status=status.HTTP_200_OK)


class AdminOrderTotalRevenueView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        total = Order.objects.aggregate(total_revenue=Sum('total'))['total_revenue'] or 0
        return Response({'total_revenue': total})


class AdminOrderTotalProductsSoldView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        result = OrderItem.objects.values('product__id', 'product__title') \
            .annotate(total_sold=Sum('quantity')) \
            .order_by('-total_sold')
        return Response(result)
