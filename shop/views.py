from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, CartItem, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.conf import settings

def product_list(request):
    products = Product.objects.filter()  # می‌تونی .filter(is_active=True) اضافه کنی
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
def _get_or_create_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_or_create_cart(request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart')

@login_required
def cart_view(request):
    cart = _get_or_create_cart(request.user)
    return render(request, 'shop/cart.html', {'cart': cart})

@login_required
def checkout(request):
    cart = _get_or_create_cart(request.user)
    if request.method == 'POST':
        # ساخت سفارش از آیتم‌های سبد
        order = Order.objects.create(user=request.user, total_amount=0)
        total = 0
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            total += item.total_price
        order.total_amount = total
        order.save()
        # پاک کردن سبد
        cart.items.all().delete()
        return redirect('my_orders')
    return render(request, 'shop/checkout.html', {'cart': cart})

@login_required
def my_orders(request):
    orders = request.user.orders.all()
    return render(request, 'shop/my_orders.html', {'orders': orders})
