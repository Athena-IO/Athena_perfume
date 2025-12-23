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
class TagSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.name', read_only=True)
    group_color = serializers.CharField(source='group.color', read_only=True)
    group_icon = serializers.CharField(source='group.icon', read_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'icon', 'group_name', 'group_color', 'group_icon']

class ProductSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'slug', 'name', 'brand', 'brand_name', 'category', 'category_name',
            'gender', 'description', 'image', 'additional_images',
            'volume_options', 'tags', 'is_active',

            # فیلدهای جدید
            'original_price', 'discount_percent', 'badge_text', 'badge_color',
            'similar_perfume', 'perfume_type', 'seasons',
            'volume', 'capacity', 'sold'
        ]

    def validate_discount_percent(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("درصد تخفیف باید بین ۰ تا ۱۰۰ باشد.")
        return value

    def validate_capacity(self, value):
        if value < 0:
            raise serializers.ValidationError("موجودی نمی‌تواند منفی باشد.")
        return value