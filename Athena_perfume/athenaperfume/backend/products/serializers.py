from rest_framework import serializers
from .models import Product, Brand, Category, Tag, TagGroup

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
            'id', 'slug', 'name', 'brand_name', 'category_name',
            'price', 'old_price', 'image', 'additional_images',
            'volume_options', 'stock', 'gender''tags', 'description'
        ]