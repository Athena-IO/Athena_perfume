from rest_framework import generics, permissions, filters
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q, F, Case, When, IntegerField
from .models import Product, Brand, Category
from .serializers import ProductSerializer, BrandSerializer, CategorySerializer
from .utils import calculate_price

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'brand__name']

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related('brand', 'category')
        
        # فیلتر بر اساس دسته‌بندی (slug)
        category_slug = self.request.query_params.get('category', None)
        if category_slug and category_slug != 'all':
            queryset = queryset.filter(category__slug=category_slug)
        
        # فیلتر بر اساس برند (slug) - پشتیبانی از چند برند
        brand_slugs = self.request.query_params.getlist('brand')
        if brand_slugs:
            queryset = queryset.filter(brand__slug__in=brand_slugs)
        
        # جستجو
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(brand__name__icontains=search_query)
            )
        
        # مرتب‌سازی
        sort_by = self.request.query_params.get('sort', None)
        if sort_by == 'price_low_high':
            # مرتب‌سازی بر اساس قیمت نهایی (با تخفیف)
            queryset = queryset.annotate(
                final_price=Case(
                    When(discount_percent__gt=0, 
                         then=F('original_price') - (F('original_price') * F('discount_percent') / 100)),
                    default=F('original_price'),
                    output_field=IntegerField()
                )
            ).order_by('final_price')
        elif sort_by == 'price_high_low':
            queryset = queryset.annotate(
                final_price=Case(
                    When(discount_percent__gt=0, 
                         then=F('original_price') - (F('original_price') * F('discount_percent') / 100)),
                    default=F('original_price'),
                    output_field=IntegerField()
                )
            ).order_by('-final_price')
        else:
            # مرتب‌سازی پیش‌فرض: موجودی بیشتر اول، سپس تاریخ ایجاد
            queryset = queryset.annotate(
                has_stock=Case(
                    When(capacity__gt=0, then=1),
                    default=0,
                    output_field=IntegerField()
                )
            ).order_by('-has_stock', '-created_at')
        
        return queryset

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
    queryset = Product.objects.filter(is_active=True).select_related('brand', 'category')
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

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


# --- ویوهای دسته‌بندی ---
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]


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