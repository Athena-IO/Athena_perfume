from rest_framework import serializers
from .models import Product, Brand, Category, Tag, TagGroup


class BrandSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug', 'logo', 'logo_url']
        read_only_fields = ['slug', 'logo_url']

    def get_logo_url(self, obj):
        if obj.logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
        read_only_fields = ['slug']


class TagSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.name', read_only=True)
    group_color = serializers.CharField(source='group.color', read_only=True)
    group_icon = serializers.CharField(source='group.icon', read_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'icon', 'group_name', 'group_color', 'group_icon']


class ProductSerializer(serializers.ModelSerializer):
    # Basic fields
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    brand_slug = serializers.CharField(source='brand.slug', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    
    # Image URLs
    image_url = serializers.SerializerMethodField()
    additional_images_urls = serializers.SerializerMethodField()
    
    # Price calculation
    price = serializers.SerializerMethodField()
    
    # Badge object (matching frontend structure)
    badge = serializers.SerializerMethodField()
    
    # Information object (matching frontend structure)
    information = serializers.SerializerMethodField()
    
    # Rating and reviews (default values, can be extended later)
    rating = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    
    # Category and brand as slugs for filtering
    category = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'slug', 'name', 
            'brand', 'brand_name', 'brand_slug',
            'category', 'category_name', 'category_slug',
            'gender', 'description', 
            'image', 'image_url', 'additional_images', 'additional_images_urls',
            'volume_options', 'tags', 'is_active',
            'original_price', 'discount_percent', 'price',
            'badge', 'badge_text', 'badge_color',
            'similar_perfume', 'perfume_type', 'seasons',
            'volume', 'capacity', 'sold',
            'information', 'rating', 'reviews'
        ]
        read_only_fields = [
            'slug', 'brand_name', 'brand_slug', 'category_name', 'category_slug',
            'image_url', 'additional_images_urls', 'price', 'badge', 'information',
            'rating', 'reviews', 'category', 'brand'
        ]

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    def get_additional_images_urls(self, obj):
        if not obj.additional_images:
            return []
        request = self.context.get('request')
        urls = []
        for img_path in obj.additional_images:
            if request:
                urls.append(request.build_absolute_uri(img_path))
            else:
                urls.append(img_path)
        return urls

    def get_price(self, obj):
        """محاسبه قیمت نهایی با در نظر گیری تخفیف"""
        if not obj.original_price:
            return 0
        if obj.discount_percent and obj.discount_percent > 0:
            discount_amount = (obj.original_price * obj.discount_percent) / 100
            return float(obj.original_price - discount_amount)
        return float(obj.original_price)

    def get_badge(self, obj):
        """ساختار badge مطابق با فرانت"""
        if obj.badge_text:
            return {
                'text': obj.badge_text,
                'color': obj.badge_color or 'primary'
            }
        return None

    def get_information(self, obj):
        """ساختار information مطابق با فرانت"""
        info = {}
        if obj.gender:
            gender_map = {
                'male': 'مردانه',
                'female': 'زنانه',
                'unisex': 'یونیسکس'
            }
            info['gender'] = gender_map.get(obj.gender, obj.gender)
        if obj.brand:
            info['brand'] = obj.brand.name
        if obj.perfume_type:
            info['type'] = obj.perfume_type
        if obj.seasons:
            # تبدیل seasons به رشته قابل نمایش
            season_map = {
                'spring': 'بهار',
                'summer': 'تابستان',
                'fall': 'پاییز',
                'winter': 'زمستان'
            }
            season_names = [season_map.get(s, s) for s in obj.seasons]
            info['season'] = ' / '.join(season_names) if season_names else None
        if obj.volume:
            info['volume'] = obj.volume
        if obj.similar_perfume:
            info['similar'] = obj.similar_perfume
        return info

    def get_rating(self, obj):
        """امتیاز محصول (می‌تواند بعداً از مدل Review اضافه شود)"""
        # فعلاً مقدار پیش‌فرض، می‌توانید بعداً از Review model استفاده کنید
        return 4.5

    def get_reviews(self, obj):
        """تعداد نظرات (می‌تواند بعداً از مدل Review اضافه شود)"""
        # فعلاً مقدار پیش‌فرض
        return 0

    def get_category(self, obj):
        """برگرداندن slug دسته‌بندی برای فیلتر"""
        return obj.category.slug if obj.category else None

    def get_brand(self, obj):
        """برگرداندن slug برند برای فیلتر"""
        return obj.brand.slug if obj.brand else None

    def validate_discount_percent(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("درصد تخفیف باید بین ۰ تا ۱۰۰ باشد.")
        return value

    def validate_capacity(self, value):
        if value < 0:
            raise serializers.ValidationError("موجودی نمی‌تواند منفی باشد.")
        return value