from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.



class UserProfile(AbstractUser):

    first_name = models.CharField(('first name'), max_length=30, null=False, blank=False)
    last_name = models.CharField(('last name'), max_length=150, null=False, blank=False)
    email = models.EmailField(('email'), unique=True, max_length=150, null=False, blank=False)
    phone = models.CharField(max_length=20, unique=True)
    country = models.CharField(max_length=20)

    is_staff = models.BooleanField(
        ('for companies :'),
        default=False,
        help_text=('If you want to register as company please click on checkbox :)'),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone', 'country']


class Product(models.Model):
    name = models.CharField(max_length=30)
    model = models.CharField(max_length=50)
    price = models.FloatField()
    max_speed = models.IntegerField()
    color = models.CharField(max_length=10)
    km_per_charge = models.IntegerField()
    manufacturing_year = models.IntegerField()
    photo = models.ImageField(upload_to='images/')
    description = models.TextField()
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    visa_card_no = models.IntegerField()
    region = models.CharField(max_length=20)
    postal_code = models.IntegerField()
    city = models.CharField(max_length=20)
    tax_registration_number = models.IntegerField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.city


class Cart(models.Model):
    OPEN, PAID, CANCELED = "open", "paid", "canceled"
    status = (
        ('open', 'Open'),
        ('paid', 'Paid'),
        ('cancel', 'Canceled')
    )

    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10, choices=status, null=True)

    def get_sum(self):
        total = 0
        for line in self.cartline_set.all():
            total += line.get_sum_price()
        return total

    # def __str__(self):
    #     return self.id


class Wishlist(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, null=True)

    # def __str__(self):
    #     return self.user_id


class CartLine(models.Model):
    quantity = models.IntegerField()
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, null=True)

    def get_sum_price(self):
        return self.quantity * self.product.price

    # def __str__(self):
    #     return self.cart_id


class WishlistLine(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True)
    wishlist = models.ForeignKey('Wishlist', on_delete=models.CASCADE, null=True)

    # def __str__(self):
    #     return self.wishlist_id
