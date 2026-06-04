from django.urls import path
from .views import checkout, my_orders

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path('my-orders/', my_orders, name='my_orders'),
]