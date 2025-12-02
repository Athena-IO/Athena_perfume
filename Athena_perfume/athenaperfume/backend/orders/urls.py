from django.urls import path
from .views import OrderListCreateView, create_order_from_cart

urlpatterns = [
    path('', OrderListCreateView.as_view(), name='order-list'),
    path('create-from-cart/', create_order_from_cart, name='create-order-from-cart'),
]