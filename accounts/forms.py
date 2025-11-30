<<<<<<< HEAD
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'company_name', 'phone', 'is_wholesaler')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'company_name', 'phone', 'is_wholesaler')
=======

>>>>>>> f269ab4 (Initial commit - Django project with MySQL setup)
