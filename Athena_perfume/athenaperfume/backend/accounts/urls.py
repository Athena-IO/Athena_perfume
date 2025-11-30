from django.urls import path
from .views import RegisterView, login_view, UserInfoView, refresh_view, logout_view  # TokenRefreshView حذف شد

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),  # custom login
    path('refresh/', refresh_view, name='refresh'),  # سفارشی
    path('userinfo/', UserInfoView.as_view(), name='userinfo'),
    path('logout/', logout_view, name='logout'),  # جدید
]