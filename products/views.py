


from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Product
from .serializers import ProductSerializer

class ProductListCreateView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        search = request.query_params.get('search', '')
        room = request.query_params.get('room', '')
        sort = request.query_params.get('sort', '')  
        

        queryset = Product.objects.filter(is_archived=False)

       
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(room__icontains=search)
            )

        
        if room:
            queryset = queryset.filter(room__iexact=room)

      
        if sort == 'lowToHigh':
            queryset = queryset.order_by('price')
        elif sort == 'highToLow':
            queryset = queryset.order_by('-price')

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk, is_archived=False)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
