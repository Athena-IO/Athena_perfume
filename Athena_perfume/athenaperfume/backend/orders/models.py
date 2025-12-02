# orders/models.py
from django.db import models
from accounts.models import CustomUser
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('processing', 'در حال پردازش'),
        ('shipped', 'ارسال شده'),
        ('delivered', 'تحویل شده'),
        ('canceled', 'لغو شده'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=12, decimal_places=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"سفارش {self.id} - {self.user.phone}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)
    product_image = models.URLField()
    volume_label = models.CharField(max_length=50)
    volume_value = models.CharField(max_length=50, blank=True, null=True)  # مثلاً "100" یا "tester"
    price = models.DecimalField(max_digits=10, decimal_places=0)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product_name} - {self.volume_label} × {self.quantity}"