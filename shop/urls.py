from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),                      # صفحه اصلی (لیست محصولات)
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),  # جزئیات محصول
    path('cart/', views.cart_view, name='cart'),                            # نمایش سبد خرید
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # افزودن محصول
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),  # حذف محصول
    path('checkout/', views.checkout, name='checkout'),                     # صفحه تسویه حساب
    path('orders/', views.my_orders, name='my_orders'),                     # سفارش‌های من
]
