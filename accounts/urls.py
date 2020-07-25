from django.contrib import admin
from django.urls import path
from products.views import UserProductHistoryView
from .views import *
app_name4='accounts'
urlpatterns = [
   path('',AccountHomeView.as_view(),name="home"),
   path('details/', UserDetailUpdateView.as_view(), name='user-update'),
   path('history/products/', UserProductHistoryView.as_view(), name='user-product-history'),
   ]
