from django.db import models
from django.utils.text import slugify


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    logo = models.ImageField(upload_to='brands/', null=True, blank=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name, allow_unicode=True)
            slug = base_slug
            i = 1
            while Brand.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    def __str__(self): return self.name


class TagGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=20, default="gray")
    def __str__(self): return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)
    group = models.ForeignKey(TagGroup, on_delete=models.CASCADE, related_name='tags')
    icon = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        unique_together = ('name', 'group')

    def __str__(self):
        return f"{self.group.name} → {self.name}"


class Product(models.Model):
    GENDER_CHOICES = (('male', 'مردانه'), ('female', 'زنانه'), ('unisex', 'یونیسکس'))

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='unisex')
    original_price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, help_text="قیمت اصلی (قبل از تخفیف)")
    discount_percent = models.PositiveIntegerField(default=0, help_text="درصد تخفیف (0-100)")
    badge_text = models.CharField(max_length=50, blank=True, help_text="متن برچسب مثل 'جدید' یا 'پرفروش'")
    badge_color = models.CharField(max_length=20, default='primary', help_text="رنگ برچسب در فرانت")

    similar_perfume = models.CharField(max_length=200, blank=True, help_text="نام عطر مشابه (مثلاً Bleu de Chanel)")
    perfume_type = models.CharField(max_length=50, blank=True, help_text="نوع عطر: EDP, EDT, ...")
    seasons = models.JSONField(default=list, blank=True, help_text='["spring", "summer", ...]')

    volume = models.CharField(max_length=20, blank=True, help_text="مثلاً 100ml")
    capacity = models.PositiveIntegerField(default=0, help_text="موجودی انبار")
    sold = models.PositiveIntegerField(default=0, help_text="تعداد فروش رفته")

    description = models.TextField()
    #price = models.DecimalField(max_digits=10, decimal_places=0)
    old_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    #stock = models.PositiveIntegerField(default=0)

    image = models.ImageField(upload_to='products/')
    additional_images = models.JSONField(default=list, blank=True)
    volume_options = models.JSONField(
        default=list,
        blank=True,
        help_text='مثال: [{"label": "۵۰ میل", "value": 50, "price": 3200000, "stock": 15}, ...]'
    )

    tags = models.ManyToManyField(Tag, blank=True, related_name='products')

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name, allow_unicode=True)
            slug = base_slug
            i = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.brand}"
    

class PricingRule(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pricing_rules')
    min_quantity = models.PositiveIntegerField(help_text="از این تعداد به بالا")
    max_quantity = models.PositiveIntegerField(
        null=True, blank=True, help_text="تا این تعداد (خالی = بدون سقف)"
    )
    price_per_unit = models.DecimalField(
        max_digits=12, decimal_places=0, help_text="قیمت هر عدد در این بازه (تومان)"
    )

    class Meta:
        ordering = ['min_quantity']
        unique_together = ('product', 'min_quantity')

    def __str__(self):
        if self.max_quantity:
            return f"{self.product.name} | {self.min_quantity}–{self.max_quantity} تایی → {self.price_per_unit:,} تومان"
        return f"{self.product.name} | {self.min_quantity} تایی به بالا → {self.price_per_unit:,} تومان"