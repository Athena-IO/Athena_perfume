from django.urls import path
from .views import RegisterView, login_view, UserInfoView, refresh_view, logout_view  # TokenRefreshView حذف شد

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),#http://127.0.0.1:8000/api/accounts/register/
    path('login/', login_view, name='login'),  # http://127.0.0.1:8000/api/accounts/login/
    path('refresh/', refresh_view, name='refresh'),  
    path('userinfo/', UserInfoView.as_view(), name='userinfo'),
    path('logout/', logout_view, name='logout'),  # http://127.0.0.1:8000/api/accounts/logout/
]



