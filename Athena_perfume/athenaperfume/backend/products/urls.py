from django.urls import path
from .views import (
    ProductListCreateView,
    ProductDetailView,
    calculate_price_view
)

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('calculate-price/<slug:slug>/', calculate_price_view, name='calculate-price'),
]