from django.contrib import admin
from django.utils.html import format_html
from .models import Banner

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_preview', 'link', 'external', 'is_active', 'order']
    list_editable = ['order', 'is_active', 'external']
    list_filter = ['is_active', 'external']
    search_fields = ['name', 'alt', 'hover_text']
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'image', 'image_preview', 'alt', 'link', 'external')
        }),
        ('تنظیمات نمایش', {
            'fields': ('hover_text', 'order', 'is_active')
        }),
    )

    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 100px; object-fit: cover; border-radius: 8px;" />', obj.image.url)
        return "(بدون تصویر)"
    image_preview.short_description = "پیش‌نمایش"