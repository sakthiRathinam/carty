from django.urls import path
from .views import *
app_name='search'
urlpatterns = [
   path('function/',SearchProductView.as_view(),name="queryy"),
   path('',searchView,name="query"),
   ]