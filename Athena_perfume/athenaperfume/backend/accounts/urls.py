from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, login_view, UserInfoView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),                # custom login
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('userinfo/', UserInfoView.as_view(), name='userinfo'),
]
