from rest_framework import serializers
from .models import Banner

class BannerSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)

    class Meta:
        model = Banner
        fields = ['id', 'name', 'image', 'link', 'order', 'is_active']
        read_only_fields = ['order']  # ترتیب خودکار یا دستی در ویو

    