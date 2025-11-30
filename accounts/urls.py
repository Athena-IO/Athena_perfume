from django.urls import path
<<<<<<< HEAD
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]
=======
from .views import RegisterView, login_view, UserInfoView, refresh_view, logout_view  # TokenRefreshView حذف شد

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),  # custom login
    path('refresh/', refresh_view, name='refresh'),  # سفارشی
    path('userinfo/', UserInfoView.as_view(), name='userinfo'),
    path('logout/', logout_view, name='logout'),  # جدید
]
>>>>>>> f269ab4 (Initial commit - Django project with MySQL setup)
