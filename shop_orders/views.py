from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import Order, OrderItem
from products.models import Product


@login_required
def checkout(request):

    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart_view')

    total = 0

    for product_id, quantity in cart.items():

        product = Product.objects.get(id=product_id)

        total += product.price * quantity

    order = Order.objects.create(
        user=request.user,
        total=total
    )

    for product_id, quantity in cart.items():

        product = Product.objects.get(id=product_id)

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )

    request.session['cart'] = {}

    return render(
    request,
    'shop_orders/order_success.html',
    {'order': order}
)


def my_orders(request):

    orders = (
        Order.objects
        .filter(user=request.user)
        .order_by('-created_at')
    )

    return render(
        request,
        'shop_orders/my_orders.html',
        {
            'orders': orders
        }
    )