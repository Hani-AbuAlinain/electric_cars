from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView, UpdateView, DetailView, ListView, DeleteView
from django.core.paginator import Paginator
from . import forms, models

# Create your views here.

from .forms import UserRegister, AddProduct, Purchase, AddCardLine
from . import models
from .help_functions import get_user_cart, get_user_wishlist
from .models import Payment, Cart, Product, UserProfile, CartLine, Wishlist, WishlistLine

"""

            INDEX VIEW

"""


@method_decorator(login_required, name="dispatch")
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        product = Product.objects.filter(user=self.request.user)
        return {'products': product}


"""

            REGISTER VIEW

"""


class RegisterView(CreateView):
    template_name = 'register.html'
    model = UserProfile
    form_class = UserRegister
    success_url = reverse_lazy('login_url')


"""  ==============================================================

                    LOGIN VIEW

==============================================================  """


class Login(LoginView):
    users = models.UserProfile.objects.all()
    template_name = 'login.html'


"""  ==============================================================
                        LOGOUT VIEW
==============================================================  """


class Logout(LogoutView):
    template_name = 'index.html'

    def logout_view(request):
        if not request.user.is_authenticated:
            return render(request, 'index.html')


"""  ==============================================================
                     PRODUCT VIEW
==============================================================  """


@login_required()
def products(request, id):
    product = models.Product.objects.filter(user=id)
    company = models.UserProfile.objects.get(id=id)

    paginator = Paginator(product, 8)

    page = request.GET.get('page')

    product = paginator.get_page(page)

    context = {
        'products': product,
        'company': company
    }

    return render(request, 'products.html', context)


"""  ==============================================================
                        PRODUCT DETAILS
==============================================================  """


@method_decorator(login_required, name='dispatch')
class ProductDetails(DetailView, CreateView):
    model = Product
    template_name = 'product_details.html'
    form_class = AddCardLine

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        cart_item = CartLine.objects.filter(product=self.get_object(), cart=get_user_cart(self.request.user))
        if cart_item.exists():
            kwargs.update({'instance': cart_item.first()})
        return kwargs


    def form_valid(self, form):
        if form.instance.pk:
            cart_line = CartLine.objects.get(pk=form.instance.pk)
            form.instance.quantity += cart_line.quantity
        form.instance.cart = get_user_cart(self.request.user)
        form.instance.product = self.get_object()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('product_details', args=(self.get_object().pk,))


"""  ==============================================================
                        ADD PRODUCT
==============================================================  """


@login_required()
@staff_member_required()
def addProduct(request):
    msg = ''

    if request.method == 'POST':
        form = AddProduct(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            msg = 'Product added successfully'
            return redirect(reverse('index'))

    else:
        form = AddProduct()

    return render(request, 'add_product_form.html', {'form': form, 'msg': msg})


"""

            DELETE PRODUCT VIEW

"""


@login_required()
@staff_member_required()
def deleteproduct(request, id):

    product = models.Product.objects.filter(id=id).delete()
    msg = 'Deleted successfully'
    return redirect(reverse('index'), {'product': product})



"""

        UPDATE GENERIC BASED VIEW  

"""


@method_decorator(login_required, name='dispatch')
@method_decorator(staff_member_required, name='dispatch')
class UpdateProductView2(UpdateView):
    model = Product
    template_name = 'update_product.html'
    form_class = forms.UpdateProduct
    success_url = reverse_lazy('index')


"""  ==============================================================
                        PRODUCT DETAILS
==============================================================  """


@method_decorator(login_required, name="dispatch")
class PurchaseProductView(CreateView, SuccessMessageMixin):
    template_name = 'purchase.html'
    model = Payment
    form_class = Purchase
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.cart = get_user_cart(self.request.user)
        return super().form_valid(form)


# -----------


class CartView(DetailView):
    model = Cart
    template_name = 'cart.html'

    def get_object(self, queryset=None):
        return get_user_cart(self.request.user)


# wish list here
class WislistView(DetailView):
    template_name = 'wishlist.html'
    model = Wishlist

    def get_object(self, queryset=None):
        return get_user_wishlist(self.request.user)


class ContactView(TemplateView):
    template_name = "conact.html"
