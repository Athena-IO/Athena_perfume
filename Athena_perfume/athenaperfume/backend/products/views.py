from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer

# لیست و ایجاد محصولات (فقط ادمین بتونه create کنه)
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['brand', 'created_by']  # فیلتر بر اساس برند یا کاربر

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [permissions.IsAdminUser]  # فقط ادمین create
        else:
            permission_classes = [permissions.AllowAny]  # لیست عمومی
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# جزئیات، بروزرسانی، حذف (فقط ادمین یا صاحب)
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]  # فقط ادمین

# API ساده برای جستجو (اختیاری)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def search_products(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(
            name__icontains=query
        ).order_by('-created_at')[:10]
    else:
        products = Product.objects.none()
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)