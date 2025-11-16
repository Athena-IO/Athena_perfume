from rest_framework import serializers
from .models import Product
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)  # فقط نمایش username
    image_url = serializers.SerializerMethodField()  # URL کامل تصویر

    class Meta:
        model = Product
        fields = ['id', 'name', 'brand', 'price', 'description', 'image', 'image_url', 'created_at', 'updated_at', 'created_by']
        read_only_fields = ['created_at', 'updated_at', 'created_by']

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url)
        return None

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("قیمت نمی‌تواند منفی باشد.")
        return value

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)