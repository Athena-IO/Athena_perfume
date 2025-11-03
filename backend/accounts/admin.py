from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'company_name', 'is_wholesaler', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('company_name','phone','is_wholesaler')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('company_name','phone','is_wholesaler')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
