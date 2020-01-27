"""

        THIS FILE FOR FUNCTIONS

"""

from app.models import Cart, Wishlist

def get_user_cart(user):
    carts = Cart.objects.filter(user=user, status=Cart.OPEN).exists()
    if carts:
        return Cart.objects.get(user=user, status=Cart.OPEN)
    return Cart.objects.create(user=user, status=Cart.OPEN)


def get_user_wishlist(user):
    wishlist = Wishlist.objects.filter(user=user).exists()
    if wishlist:
        return wishlist.objects.get(user=user)
    return Wishlist.objects.create()




