from rest_framework import generics, permissions , filters
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import Product, Brand 
from .serializers import ProductSerializer, BrandSerializer
from .utils import calculate_price

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]  
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'brand__name']  # جستجو در نام محصول و نام برند

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related('brand')
        
        # جستجوی پیشرفته (partial match)
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(brand__name__icontains=search_query)
            )
        
        return queryset.order_by('-created_at')

class ProductAdminView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        # ادمین همه رو ببینه (حتی غیرفعال)
        return Product.objects.all().select_related('brand')

    def perform_create(self, serializer):
        # slug خودکار
        serializer.save()




class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAdminUser]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


# --- ویوهای برند ---
class BrandListCreateView(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class BrandDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'slug'


# --- محاسبه قیمت بر اساس تعداد ---
@api_view(['GET'])
def calculate_price_view(request, slug):
    try:
        qty = int(request.query_params.get('qty', 1))
        if qty < 1:
            return Response({"error": "تعداد باید حداقل ۱ باشد"}, status=400)

        product = Product.objects.get(slug=slug, is_active=True)
        price = calculate_price(product, qty)

        return Response({
            "product": product.name,
            "quantity": qty,
            "price_per_unit": price,
            "total_price": price * qty,
            "currency": "تومان"
        })

    except Product.DoesNotExist:
        return Response({"error": "محصول یافت نشد"}, status=404)
    except ValueError as e:
        return Response({"error": str(e)}, status=400)