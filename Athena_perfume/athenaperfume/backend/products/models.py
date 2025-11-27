from django.db import models
from django.utils.text import slugify


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='brands/', null=True, blank=True)
    def __str__(self): return self.name


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

    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    old_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)

    image = models.ImageField(upload_to='products/')
    additional_images = models.JSONField(default=list, blank=True)
    volume_options = models.JSONField(default=list)

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