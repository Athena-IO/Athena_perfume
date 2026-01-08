from django.db import models

class Banner(models.Model):
    name = models.CharField(max_length=200, help_text="نام بنر برای شناسایی (مثلاً: فروش تابستان)")
    image = models.ImageField(upload_to='banners/', help_text="اندازه پیشنهادی: 1920x600")
    link = models.CharField(max_length=500, blank=True, null=True, help_text="لینک اختیاری (مثلاً /products/sale)")
    alt = models.CharField(max_length=200, blank=True, help_text="متن alt برای تصویر (اگر خالی باشد از name استفاده می‌شود)")
    external = models.BooleanField(default=False, help_text="اگر true باشد، لینک در تب جدید باز می‌شود")
    hover_text = models.CharField(max_length=200, blank=True, help_text="متن tooltip هنگام hover (اختیاری)")
    order = models.PositiveIntegerField(default=0, help_text="ترتیب نمایش (کمتر = بالاتر)")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "بنر"
        verbose_name_plural = "بنرها"

    def __str__(self):
        return self.name
