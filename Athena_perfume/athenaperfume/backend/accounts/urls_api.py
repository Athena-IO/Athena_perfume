# accounts/urls_api.py
from django.urls import path
from .views import login_view, logout_view, refresh_view

urlpatterns = [
    path('login/', login_view, name='login'),      # ← فقط 'login/' بدون api/
    path('logout/', logout_view, name='logout'),
    path('refresh/', refresh_view, name='refresh'),
]