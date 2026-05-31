from django.shortcuts import redirect, render, get_object_or_404 # type: ignore
from .models import Product

def product_list(request):
    products = Product.objects.all()

    return render(request, 'products/product_list.html', {
        'products': products

    })

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    return render(request, 'products/product_detail.html', {
        'product': product
    })

def add_to_cart(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)] += 1
    else:
        cart[str(id)] = 1

    request.session['cart'] = cart

    return redirect('cart_view')

def remove_from_cart(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        del cart[str(id)]

    request.session['cart'] = cart

    return redirect('cart_view')



def cart_view(request):
    cart = request.session.get('cart', {})

    products = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)

        product.total_price = product.price * quantity
        product.quantity = quantity

        total += product.total_price
        products.append(product)

    return render(request, 'products/cart.html', {
        'products': products,
        'total': total
    })

def increase_quantity(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)] += 1

    request.session['cart'] = cart

    return redirect('cart_view')

def decrease_quantity(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)] -= 1

        if cart[str(id)] <= 0:
            del cart[str(id)]

    request.session['cart'] = cart

    return redirect('cart_view')