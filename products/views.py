from django.db.models import Q # type: ignore
from django.shortcuts import redirect, render, get_object_or_404 # type: ignore
from .models import Product, Category, Review,Wishlist
from django.contrib.auth.decorators import login_required

from .forms import ReviewForm

def product_list(request):

    products = Product.objects.all()

    categories = Category.objects.all()

    search = request.GET.get('search')

    category_id = request.GET.get('category')

    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(brand__icontains=search)
        )

    if category_id:
        products = products.filter(
            category_id=category_id
        )

    return render(
        request,
        'products/product_list.html',
        {
            'products': products,
            'categories': categories
        }
    )

def product_detail(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    if request.method == 'POST':

        if request.user.is_authenticated:

            form = ReviewForm(
                request.POST
            )

            if form.is_valid():

                review = form.save(
                    commit=False
                )

                review.user = request.user
                review.product = product

                review.save()

                return redirect(
                    'product_detail',
                    id=id
                )

    else:
        form = ReviewForm()

    reviews = product.reviews.all()

    return render(
        request,
        'products/product_detail.html',
        {
            'product': product,
            'reviews': reviews,
            'form': form
        }
    )

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

@login_required
def add_to_wishlist(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect(
        'product_detail',
        id=id
    )

@login_required
def wishlist(request):

    items = Wishlist.objects.filter(
        user=request.user
    )

    return render(
        request,
        'products/wishlist.html',
        {
            'items': items
        }
    )

@login_required
def remove_from_wishlist(request, id):

    Wishlist.objects.filter(
        user=request.user,
        product_id=id
    ).delete()

    return redirect('wishlist')