from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static


from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns =[
    path('', views.index, name="index"),
    path('registerclass/', views.RegisterView.as_view(), name="register"),

    path('reg_company/', views.register_company, name="reg_company"),

    path('login/', views.Login.as_view(), name="login_url"),
    path('index', views.Logout.as_view(), name="logout"),


    path('companyindex/', views.index, name="companyindex"),
    path('addproduct/', views.addProduct, name="addproduct"),

    path('deleteproduct/<int:id>/', views.deleteproduct, name="deleteproduct"),
    # path('delete-product/<int:id>', views.DeleteProductView.as_view(), name="deleteproduct"),
    path('updateproduct2/<int:pk>/', views.UpdateProductView2.as_view(), name="updateproduct2"),



    path("products/<int:id>/", views.products, name="product"),
    # path('productdetails/<int:id>', views.productDetails, name="productDetails"),
    path("product-details/<int:pk>/", views.ProductDetails.as_view(), name="product_details"),



    # path('cart/<int:id>', views.cart, name="cart"),
    path("cart/", views.CartView.as_view(), name="cart"),
    path("wishlist/", views.WislistView.as_view(), name="wishlist"),

    path("contact/", views.ContactView.as_view(), name="contact"),


    path('purchaseproduct/<int:pk">', views.PurchaseProductView.as_view(), name='purchaseproduct'),

    # path('cartl/<int:pk>', views.addCartline, name="cartlines"),

    # path('base/', views.base_, name="base"),


]

