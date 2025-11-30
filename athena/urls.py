from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('accounts/', include('accounts.urls')),   # routes related to auth
    path('', include('shop.urls')),                # shop main pages
=======
    path('api/accounts/', include('accounts.urls')),
    path('api/products/', include('products.urls')), 
>>>>>>> f269ab4 (Initial commit - Django project with MySQL setup)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
<<<<<<< HEAD
=======

>>>>>>> f269ab4 (Initial commit - Django project with MySQL setup)
