from django.contrib import admin # type: ignore
from .models import Product, Category, Review, Wishlist

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Wishlist)