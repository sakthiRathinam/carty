from django.urls import path
from .views import *
app_name='cart'
urlpatterns = [
   path('',cart_home,name="home"),
   path('update/',cart_update,name="update"),
   path('checkout/',checkoutProcess,name="checkout"),
   path('checkout/success',checkout_success,name="success"),
   ]