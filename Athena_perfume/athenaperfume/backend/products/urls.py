from django.urls import path
from .views import ProductListCreateView, ProductDetailView, search_products

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('search/', search_products, name='search-products'),
]