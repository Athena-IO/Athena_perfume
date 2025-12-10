from rest_framework import generics, permissions
from .models import Product
from .serializers import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import calculate_price

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]  # فقط ادمین بتونه ایجاد کنه

    def perform_create(self, serializer):
        serializer.save()

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAdminUser]  # فقط ادمین ویرایش/حذف کنه

    def perform_destroy(self, instance):
        instance.is_active = False  # soft delete
        instance.save()


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