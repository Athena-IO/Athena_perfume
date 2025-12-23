from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product, Brand 
from .serializers import ProductSerializer, BrandSerializer
from .utils import calculate_price


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]  # فقط ادمین بتونه اضافه کنه

    def perform_create(self, serializer):
        # slug خودکار اگر خالی بود
        if not serializer.validated_data.get('slug'):
            name = serializer.validated_data['name']
            slug = slugify(name, allow_unicode=True)
            i = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{slugify(name, allow_unicode=True)}-{i}"
                i += 1
            serializer.save(slug=slug)
        else:
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