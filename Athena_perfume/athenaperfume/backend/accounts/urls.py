from django.urls import path
from .views import RegisterView, login_view, UserInfoView, refresh_view, logout_view  # TokenRefreshView حذف شد

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),  # custom login
    path('refresh/', refresh_view, name='refresh'),  # سفارشی
    path('userinfo/', UserInfoView.as_view(), name='userinfo'),
    path('logout/', logout_view, name='logout'),  # جدید
]
from django.urls import path
from .views import login_view, refresh_view, logout_view, UserInfoView, LoginLogListView

urlpatterns = [
    path('login/', login_view, name='login'),
    path('refresh/', refresh_view, name='refresh'),
    path('logout/', logout_view, name='logout'),
    path('me/', UserInfoView.as_view(), name='user_info'),

    # مشاهده لاگ‌های ورود
    path('login-logs/', LoginLogListView.as_view(), name='login_logs'),
]

from django.urls import path, include

urlpatterns = [
    # ... الگوهای موجود شما
    path('accounts/', include('django.contrib.auth.urls')),
]