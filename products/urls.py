from django.urls import path
from .views import product_list, product_detail, add_to_cart, cart_view, remove_from_cart, increase_quantity, decrease_quantity

urlpatterns = [
    path('', product_list, name='product_list'),
    path('product/<int:id>/', product_detail, name='product_detail'),

    path('cart/', cart_view, name='cart_view'),
    path('cart/add/<int:id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:id>/', remove_from_cart, name='remove_from_cart'),

    path('cart/increase/<int:id>/', increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:id>/', decrease_quantity, name='decrease_quantity'),

]