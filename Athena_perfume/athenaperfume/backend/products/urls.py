from django.urls import path
from .views import (
   ProductListCreateView, ProductDetailView,
    BrandListCreateView, BrandDetailView,
    calculate_price_view
)

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list-create'),#http://127.0.0.1:8000/api/products/
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),#http://127.0.0.1:8000/api/products/sauvage-elixir/
    path('calculate-price/<slug:slug>/', calculate_price_view, name='calculate-price'),#http://127.0.0.1:8000/api/products/calculate-price/sauvage-elixir/?qty=5
    path('brands/', BrandListCreateView.as_view(), name='brand-list-create'),
    path('brands/<slug:slug>/', BrandDetailView.as_view(), name='brand-detail'),
]