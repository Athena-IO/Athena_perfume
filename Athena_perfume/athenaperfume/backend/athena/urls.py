from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products.views import CategoryListView, CategoryDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/products/', include('products.urls')),
    path('api/orders/', include('orders.urls')),  
    path('api/banners/', include('banners.urls')),
    # Categories API (matching frontend expectation)
    path('api/categories/', CategoryListView.as_view(), name='category-list'),
    path('api/categories/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)