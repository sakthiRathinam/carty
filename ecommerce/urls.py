"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings 
from .views import *
from addresses.views import *
from cart.views import cart_api_view
from accounts.views import *
from billing.views import *
from products.views import *
from analytics.views import *
from django.views.generic import TemplateView, RedirectView
app_name='products'
app_name1='search'
app_name2='cart'
app_name3='orders'
app_name4='accounts'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',ProductListView.as_view(),name="list"),
    path('sales/',SalesView.as_view(),name="sales"),
    path('sales/data/',SalesAjaxView.as_view(),name="salesData"),
    path('api/cart/', cart_api_view, name='api-cart'),
    path('accounts/', include("accounts.passwords.urls")),
    path('accounts/', RedirectView.as_view(url='/account')),
    path('guestProfile/',guestView,name="guest"),
    path('billing/payment-method/create/', payment_method_createview, name='billing-payment-method-endpoint'),
    path('paymentMethod/',payment_method,name="payment"),
    path('address/',checkout_address_create_view, name='checkout_address_create'),
    path('checkout/address/reuse/', checkout_address_reuse_view, name='checkout_address_reuse'),
    path('products/',include(("products.urls",app_name),namespace='products')),
    path('products/search/',include(("search.urls",app_name1),namespace='search')),
    path('cart/',include(("cart.urls",app_name2),namespace='cart')),
    path('account/',include(("accounts.urls",app_name4),namespace='account')),
    path('order/',include(("orders.urls",app_name3),namespace='order')),
    path('login/',loginPage,name="login"),
    path('logout/',logoutUser,name="logout"),
    path('register/',register_page,name="register"),
    path('contact/',contactPage,name="contact"),
]

if settings.DEBUG:
	urlpatterns=urlpatterns+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
	urlpatterns=urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)