from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView, UpdateView, DetailView, ListView, DeleteView
from django.core.paginator import Paginator

from . import forms, models

# Create your views here.

from .forms import UserRegister, AddProduct, UpdateProduct, Purchase, AddCardLine
from . import models
from .models import Payment, Cart, Product, UserProfile, CartLine, Wishlist

"""

            INDEX VIEW

"""


# @login_required
def index(request):
    product = models.Product.objects.filter(user=request.user.id)
    user_product = Product.objects.all()

    paginator = Paginator(user_product, 8)

    page = request.GET.get('page')

    user_product = paginator.get_page(page)

    context = {
        'products': product,
        'user_product': user_product
    }

    return render(request, 'index.html', context)


"""

            REGISTER VIEW

"""


class RegisterView(CreateView):
    template_name = 'register.html'
    model = UserProfile
    form_class = UserRegister

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('login_url')



"""  ==============================================================
                    REGISTER COMPANY VIEW
==============================================================  """


#not working
def register_company(request):
    user = models.UserProfile.objects.all()
    return render(request, 'registercompany.html', {'users': user})


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


@login_required()
def productDetails(request, id):
    product = Product.objects.get(id=id)
    form = AddCardLine()

    context = {
        'products': product,
        'form': form
    }
    return render(request, 'product_details.html', context)


"""  =============================================================
                            CLASS PRODUCT VIEW
============================================================== """


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
            # form = AddProduct()
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


# class DeleteProductView(DeleteView):
#     template_name = 'index.html'
#     model = Product
#     # success_url = redirect(reverse('index'))
#
#     def get_object(self):
#         id = self.kwargs.get("id")
#         return get_object_or_404(self.model, id=id)
#
#     def get_success_url(self):
#         return reverse('index')
#


"""

            UPDATE PRODUCT VIEW

"""


@login_required
@staff_member_required
def updateproduct(request, id):
    msg = ''
    instance = models.Product.objects.get(id=id)
    form = AddProduct(request.POST or None, request.FILES or None, instance=instance)

    if form.is_valid():
        form.instance.user = request.user
        form.save()
        return redirect(reverse('index'))

    context = {
        'form': form,
        'msg': msg,
    }

    return render(request, 'update_product.html', context)


class UpdateProductView(TemplateView):
    template_name = 'update_product.html'

    def get(self, request, id):
        instance = models.Product.objects.get(id=id)
        form = UpdateProduct(instance=instance)

        args = {'form': form}
        return render(request, self.template_name, args)

    def post(self, request, id):
        instance = models.Product.objects.get(id=id)
        form = UpdateProduct(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('index')

        args = {'form': form}
        return render(request, self.template_name, args)


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
class PurchaseProductView(CreateView):
    template_name = 'purchase.html'
    model = Payment
    form_class = Purchase
    # fields = ['all']
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.cart = get_user_cart(self.request.user)
        return super().form_valid(form)






# @login_required()
# def purchaseProduct(request, id):
#     product = models.Product.objects.filter(id=id)
#     company = models.UserProfile.objects.filter(is_superuser=False, is_staff=True)
#     # instance = models.Product.objects.get(id=id)
#
#     if request.method == "POST":
#         form = forms.Purchase(request.POST or None)
#         if form.is_valid():
#             form.instance.user = request.user
#             form.instance.card = request.card
#             form.save()
#             # form = Purchase()
#             # return render(request, 'index.html')
#             return redirect(reverse('index'))
#     else:
#         form = Purchase()
#
#     context = {
#         'products': product,
#         'companies': company,
#         'form': form,
#         }
#
#     return render(request, 'purchase.html', context)


def get_user_cart(user):
    carts = Cart.objects.filter(user=user, status=Cart.OPEN).exists()
    if carts:
        return Cart.objects.get(user=user, status=Cart.OPEN)
    return Cart.objects.create(user=user, status=Cart.OPEN)


# -----------

class CartView(DetailView):
    model = Cart
    template_name = 'cart.html'

    def get_object(self, queryset=None):
        return get_user_cart(self.request.user)


# wish list here

def get_user_wishlist(user):
    wishlist = Wishlist.objects.get(user=user)
    return wishlist


class WislistView(DetailView):
    template_name = 'wishlist.html'
    model = Wishlist

    def get_object(self, queryset=None):
        return get_user_wishlist(self.request.user)


class ContactView(TemplateView):
    template_name = "conact.html"

