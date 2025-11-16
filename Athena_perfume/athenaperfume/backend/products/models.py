from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام محصول")
    brand = models.CharField(max_length=100, verbose_name="برند")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت (تومان)")
    description = models.TextField(verbose_name="توضیحات")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="تصویر")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', verbose_name="ایجادکننده")

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.brand}"