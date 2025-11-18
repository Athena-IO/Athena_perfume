from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),  # register, me, login-logs و ...
    path('api/products/', include('products.urls')),

    # این سه تا باعث میشه مستقیم این آدرس‌ها کار کنن:
    # → http://127.0.0.1:8000/login/
    # → http://127.0.0.1:8000/logout/
    # → http://127.0.0.1:8000/refresh/
    path('', include('accounts.urls_api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)