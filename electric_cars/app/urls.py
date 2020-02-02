from django.urls import path
from . import views

urlpatterns =[
    # path(' ', views.IndexView.as_view(), name='index'),
    path('registerclass/', views.RegisterView.as_view(), name="register"),

    path('login/', views.Login.as_view(), name="login_url"),
    path('index', views.Logout.as_view(), name="logout"),

    path("products/<int:id>/", views.products, name="product"),
    path('addproduct/', views.addProduct, name="addproduct"),

    path('deleteproduct/<int:id>/', views.deleteproduct, name="deleteproduct"),
    path('update-product2/<int:pk>/', views.UpdateProductView2.as_view(), name="updateproduct2"),

    path("product-details/<int:pk>/", views.ProductDetails.as_view(), name="product_details"),
    path("cart/", views.CartView.as_view(), name="cart"),

    path("wishlist/", views.WislistView.as_view(), name="wishlist"),
    path("contact/", views.ContactView.as_view(), name="contact"),

    path('purchaseproduct/<int:pk">', views.PurchaseProductView.as_view(), name='purchaseproduct'),
]

