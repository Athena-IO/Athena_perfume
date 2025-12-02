from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product_slug', 'product_name', 'product_image', 'volume_label', 'price', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'total_amount', 'status', 'status_display', 'created_at', 'paid_at', 'items']
        read_only_fields = ['total_amount', 'status', 'created_at', 'paid_at']