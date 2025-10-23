from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Product
from .serializers import ProductSerializer

class ProductListCreateView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        search = request.query_params.get('search')
        queryset = Product.objects.filter(is_archived=False)
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search) | Q(room__icontains=search))
        return Response(ProductSerializer(queryset, many=True).data)

    def post(self, request):
        if not request.user.is_staff:
            return Response({'error': 'Only admins can add products'}, status=403)
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(ProductSerializer(product).data, status=201)
        return Response(serializer.errors, status=400)

class ProductDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk, is_archived=False)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)
        return Response(ProductSerializer(product).data)
