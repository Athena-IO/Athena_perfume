# orders/views.py
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db import transaction
from .models import Order, OrderItem
from .serializers import OrderSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@transaction.atomic  # اگه خطا داد، همه چیز rollback بشه
def create_order_from_cart(request):
    cart_items = request.data.get('cart')

    # چک کردن وجود سبد
    if not cart_items or not isinstance(cart_items, list) or len(cart_items) == 0:
        return Response(
            {"detail": "سبد خرید خالی است یا فرمت اشتباه است."},
            status=status.HTTP_400_BAD_REQUEST
        )

    total_amount = 0
    order_items_data = []

    # اعتبارسنجی و محاسبه قیمت کل
    for item in cart_items:
        try:
            price = float(item['price'])
            qty = int(item['qty'])
            if qty <= 0:
                return Response({"detail": f"تعداد نامعتبر برای {item.get('name', 'محصول')}"})
        except (KeyError, TypeError, ValueError):
            return Response(
                {"detail": "داده‌های سبد خرید نامعتبر است."},
                status=status.HTTP_400_BAD_REQUEST
            )

        total_amount += price * qty

        order_items_data.append({
            'product_slug': item.get('slug', ''),
            'product_name': item.get('name', 'نامشخص'),
            'product_image': item.get('image', ''),
            'volume_label': item.get('volumeLabel', 'نامشخص'),
            'price': price,
            'quantity': qty,
        })

    # ساخت سفارش
    order = Order.objects.create(
        user=request.user,
        total_amount=int(total_amount),  # ذخیره به صورت عدد صحیح (تومان)
        status='pending'
    )

    # ساخت آیتم‌های سفارش
    order_items = [
        OrderItem(order=order, **data)
        for data in order_items_data
    ]
    OrderItem.objects.bulk_create(order_items)

    return Response({
        "order_id": order.id,
        "total_amount": int(total_amount),
        "items_count": len(order_items),
        "message": "سفارش با موفقیت ثبت شد. در انتظار پرداخت..."
    }, status=status.HTTP_201_CREATED)