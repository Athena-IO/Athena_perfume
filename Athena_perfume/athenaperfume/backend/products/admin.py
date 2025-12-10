# products/admin.py

from django.contrib import admin
from .models import Brand, Category, TagGroup, Tag, Product
from .models import PricingRule

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(TagGroup)
class TagGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'icon']
    search_fields = ['name']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'group']
    list_filter = ['group']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'gender', 'is_active', 'created_at']
    list_filter = ['brand', 'category', 'gender', 'is_active']
    search_fields = ['name', 'brand__name']
    filter_horizontal = ['tags']


@admin.register(PricingRule)
class PricingRuleAdmin(admin.ModelAdmin):
    list_display = ['product', 'min_quantity', 'max_quantity', 'price_per_unit']
    list_filter = ['product__brand', 'product__name']
    search_fields = ['product__name']