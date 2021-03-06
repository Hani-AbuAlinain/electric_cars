from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile, Product
from . import models


class UserRegister(UserCreationForm):
    class Meta:
        model = UserProfile

        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'country', 'password1', 'password2',
                  'is_staff']


class UserLogin(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = {'email', 'password'}


class AddProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'model', 'price', 'max_speed', 'color',
                  'km_per_charge', 'manufacturing_year', 'photo', 'description']


class UpdateProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'model', 'price', 'max_speed', 'color',
                  'km_per_charge', 'manufacturing_year', 'photo', 'description']


class Purchase(forms.ModelForm):
    class Meta:
        model = models.Payment
        fields = ['visa_card_no', 'region', 'postal_code', 'city', 'tax_registration_number']


class AddCardLine(forms.ModelForm):
    class Meta:
        model = models.CartLine
        fields = ['quantity']


class AddWishlistLine(forms.ModelForm):
    class Meta:
        model = models.WishlistLine
        fields = []
