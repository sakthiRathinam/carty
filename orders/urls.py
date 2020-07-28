from django.urls import path
from .views import *
app_name='orders'
urlpatterns = [
path('', OrderListView.as_view(), name='list'),
path('detail/<str:order_id>/', OrderDetailView.as_view(), name='detail'),
path('library/', LibraryView.as_view(), name='library'),
path('owner/', VerifyOwnership.as_view(), name='verify'),
   ]