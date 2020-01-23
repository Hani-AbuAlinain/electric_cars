from .models import Cart, UserProfile
from .views import get_user_cart


def passing_cart(request):
    if request.user.is_authenticated:
        cart = get_user_cart(request.user)
        return {"cart": cart}
    return {}


def dropdowm_company(req):
    company = UserProfile.objects.filter(is_staff=True, is_superuser=False)
    return {"companies": company}

