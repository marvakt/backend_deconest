


# from rest_framework import permissions
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import CartItem
# from .serializers import CartItemSerializer

# # ---------------- Single Cart Item Operations ----------------
# class CartView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         items = CartItem.objects.filter(user=request.user)
#         return Response(CartItemSerializer(items, many=True).data)

#     def post(self, request):
#         serializer = CartItemSerializer(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         product = serializer.validated_data['product']
#         quantity = serializer.validated_data.get('quantity', 1)
#         item, created = CartItem.objects.get_or_create(
#             user=request.user,
#             product=product,
#             defaults={'quantity': quantity}
#         )
#         if not created:
#             item.quantity += quantity
#             item.save()
#         return Response(CartItemSerializer(item, context={'request': request}).data, status=201)

#     def put(self, request, pk):
#         try:
#             item = CartItem.objects.get(pk=pk, user=request.user)
#         except CartItem.DoesNotExist:
#             return Response({'error': 'Item not found'}, status=404)
#         serializer = CartItemSerializer(item, data=request.data, partial=True, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def delete(self, request, pk):
#         try:
#             item = CartItem.objects.get(pk=pk, user=request.user)
#             item.delete()
#             return Response({'message': 'Item removed'}, status=204)
#         except CartItem.DoesNotExist:
#             return Response({'error': 'Item not found'}, status=404)

# # ---------------- Clear All Cart Items ----------------
# class ClearCartView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def delete(self, request):
#         CartItem.objects.filter(user=request.user).delete()
#         return Response({"message": "Cart cleared"}, status=204)




from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CartItem, Product
from .serializers import CartItemSerializer

# ---------------- Single Cart Item Operations ----------------
class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        items = CartItem.objects.filter(user=request.user)
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        if not product_id:
            return Response({"error": "Product ID is required"}, status=400)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={"quantity": quantity}
        )

        if not created:
            item.quantity += int(quantity)
            item.save()

        serializer = CartItemSerializer(item)
        return Response(serializer.data, status=201)

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

    def delete(self, request, pk):
        try:
            item = CartItem.objects.get(pk=pk, user=request.user)
            item.delete()
            return Response({"message": "Item removed"}, status=204)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)


# ---------------- Clear Entire Cart ----------------
class ClearCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        CartItem.objects.filter(user=request.user).delete()
        return Response({"message": "Cart cleared"}, status=204)
