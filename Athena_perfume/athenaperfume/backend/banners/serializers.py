from rest_framework import serializers
from .models import Banner

class BannerSerializer(serializers.ModelSerializer):
    # Image URL for frontend
    image_url = serializers.SerializerMethodField()
    
    # URL alias for frontend compatibility (link -> url)
    url = serializers.SerializerMethodField()
    
    # Alt text (use name if alt is empty)
    alt = serializers.SerializerMethodField()
    
    # Hover text (camelCase for frontend)
    hoverText = serializers.SerializerMethodField()
    
    # External flag
    external = serializers.BooleanField(default=False)

    class Meta:
        model = Banner
        fields = [
            'id', 'name', 'image', 'image_url', 
            'link', 'url', 'alt', 'external', 
            'hover_text', 'hoverText', 'order', 'is_active'
        ]
        read_only_fields = ['order', 'image_url', 'url', 'alt', 'hoverText']

    def get_image_url(self, obj):
        """برگرداندن URL کامل تصویر"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    def get_url(self, obj):
        """برگرداندن link با نام url برای سازگاری با فرانت"""
        return obj.link or ''

    def get_alt(self, obj):
        """برگرداندن alt یا name به عنوان fallback"""
        return obj.alt or obj.name

    def get_hoverText(self, obj):
        """برگرداندن hover_text با نام camelCase"""
        return obj.hover_text or ''

    