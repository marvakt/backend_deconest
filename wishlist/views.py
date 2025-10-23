from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Wishlist
from .serializers import WishlistSerializer

class WishlistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        wishlist_items = Wishlist.objects.filter(user=request.user)
        return Response(WishlistSerializer(wishlist_items, many=True).data)

    def post(self, request):
        serializer = WishlistSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            product = serializer.validated_data['product']
            if Wishlist.objects.filter(user=request.user, product=product).exists():
                return Response({'error': 'Already in wishlist'}, status=400)
            item = serializer.save()
            return Response(WishlistSerializer(item).data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            item = Wishlist.objects.get(pk=pk, user=request.user)
            item.delete()
            return Response({'message': 'Removed from wishlist'}, status=204)
        except Wishlist.DoesNotExist:
            return Response({'error': 'Item not found'}, status=404)
