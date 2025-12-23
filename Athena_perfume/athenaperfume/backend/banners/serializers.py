from rest_framework import serializers
from .models import Banner

class BannerSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)

    class Meta:
        model = Banner
        fields = ['id', 'name', 'image', 'link', 'order', 'is_active']
        read_only_fields = ['order']  # ترتیب خودکار یا دستی در ویو

    def validate(self, data):
        # حداکثر ۴ بنر
        if self.context['request'].method == 'POST':
            current_count = Banner.objects.count()
            if current_count >= 4:
                raise serializers.ValidationError("حداکثر ۴ بنر مجاز است.")
        return data