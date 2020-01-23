from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Product, UserProfile, Payment, Cart, CartLine, Wishlist, WishlistLine

# Register your models here.

classes = [Product, Payment, Cart, CartLine, Wishlist, WishlistLine]
admin.site.register(classes)

admin.site.register(UserProfile, UserAdmin)
