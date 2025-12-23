from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ['phone', 'username', 'email', 'role', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    search_fields = ['phone', 'username', 'email']
    ordering = ['-date_joined']

    fieldsets = (
        ('اطلاعات شخصی', {'fields': ('username', 'email', 'phone', 'password')}),
        ('نقش و دسترسی', {'fields': ('role', 'is_staff', 'is_superuser', 'is_active')}),
        ('تاریخ‌ها', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'username', 'email', 'password1', 'password2', 'role', 'is_active'),
        }),
    )

    readonly_fields = ['date_joined', 'last_login']